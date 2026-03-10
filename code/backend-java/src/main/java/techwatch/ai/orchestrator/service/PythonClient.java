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

    public PythonClient(@Value("${app.python-service.url:http://localhost:8000}") String pythonUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(pythonUrl)
                .build();
    }

    /**
     * Asynchronously triggers the Python worker to process and enrich an article.
     *
     * @param articleId the unique identifier of the article to process
     */
    @Async
    public void triggerEnrichment(UUID articleId) {
        String uri = "/api/v1/articles/" + articleId + "/process";

        log.info("Triggering async enrichment via Python worker for article: {}", articleId);

        try {
            restClient.post()
                    .uri(uri)
                    .retrieve()
                    .toBodilessEntity();

            log.debug("Enrichment successfully triggered for article: {}", articleId);

        } catch (Exception e) {
            log.error("Failed to trigger Python worker for article {}. Error: {}", articleId, e.getMessage());
        }
    }
}