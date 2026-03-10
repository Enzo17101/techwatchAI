package techwatch.ai.orchestrator.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import techwatch.ai.orchestrator.entity.Article;
import techwatch.ai.orchestrator.repository.ArticleRepository;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class ResilienceService {

    private final ArticleRepository articleRepository;
    private final PythonClient pythonClient;

    /**
     * Le "Balayeur" (Sweep Job).
     * Tourne toutes les 2 heures (7200000 ms), 5 minutes après le démarrage (300000 ms).
     * Son rôle est de trouver les articles oubliés ou plantés et de les relancer.
     */
    @Scheduled(initialDelay = 300000, fixedRate = 7200000)
    public void retryIncompleteArticles() {
        log.info("Starting Resilience Sweep: Looking for incomplete articles in DB...");

        List<Article> incompleteArticles = articleRepository.findIncompleteArticles();

        if (incompleteArticles.isEmpty()) {
            log.info("Resilience Sweep finished: All articles are fully processed. Good job!");
            return;
        }

        log.warn("Resilience Sweep found {} incomplete articles. Retriggering AI processing...", incompleteArticles.size());

        for (Article article : incompleteArticles) {
            log.debug("Retrying article: {}", article.getTitle());
            // Appel asynchrone vers Python
            pythonClient.triggerEnrichment(article.getId());
        }
    }
}