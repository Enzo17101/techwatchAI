package techwatch.ai.orchestrator.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.UUID;

@Slf4j
@Service
public class PythonClient {

    private final RestClient restClient;

    // On prépare l'URL de base (localhost:8000 pour l'instant)
    public PythonClient(@Value("${app.python-service.url:http://localhost:8000}") String pythonUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(pythonUrl)
                .build();
    }

    /**
     * Appelle le service Python pour enrichir l'article.
     * @Async : Cette méthode s'exécute dans un thread séparé.
     * Le RssService n'attendra pas la fin de son exécution.
     */
    @Async
    public void triggerEnrichment(UUID articleId) {
        String uri = "/api/v1/articles/" + articleId + "/process";

        log.info("Async call to Python Worker for article: {}", articleId);

        try {
            // Appel POST sans corps (puisque l'ID est dans l'URL)
            restClient.post()
                    .uri(uri)
                    .retrieve()
                    .toBodilessEntity(); // On ignore la réponse, on veut juste déclencher

            log.debug("Python enrichment triggered successfully for {}", articleId);

        } catch (Exception e) {
            // En asynchrone, il est vital de logger les erreurs car personne ne les attrapera plus haut
            log.error("Failed to call Python service for article {}: {}", articleId, e.getMessage());
        }
    }
}