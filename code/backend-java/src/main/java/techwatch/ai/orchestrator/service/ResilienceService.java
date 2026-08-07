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
     * Background sweep job designed to find and retrigger articles that failed processing.
     * Runs every 2 hours, with an initial delay of 5 minutes after startup.
     */
    @Scheduled(initialDelay = 120000, fixedRate = 7200000)
    public void retryIncompleteArticles() {
        log.info("Starting resilience sweep: Scanning database for incomplete articles...");

        List<Article> incompleteArticles = articleRepository.findIncompleteArticles();

        if (incompleteArticles.isEmpty()) {
            log.info("Resilience sweep completed: No pending or failed articles found.");
            return;
        }

        log.warn("Resilience sweep identified {} incomplete articles. Triggering AI processing retries...", incompleteArticles.size());

        for (Article article : incompleteArticles) {
            log.debug("Scheduling retry for article ID: {}", article.getId());
            pythonClient.triggerEnrichment(article.getId());
        }
    }
}