package techwatch.ai.orchestrator.service;

import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndFeed;
import com.rometools.rome.io.SyndFeedInput;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.xml.sax.InputSource;
import techwatch.ai.orchestrator.entity.Article;
import techwatch.ai.orchestrator.repository.ArticleRepository;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class RssService {

    private final ArticleRepository articleRepository;
    private final PythonClient pythonClient;

    @Value("${app.user-agent:TechWatch-AI/1.0}")
    private String userAgent;

    private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .build();

    public void fetchRssFeed(String feedUrl) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(feedUrl))
                    .header("User-Agent", userAgent)
                    .GET()
                    .build();

            HttpResponse<InputStream> response = HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofInputStream());

            if (response.statusCode() != 200) {
                log.warn("Feed unreachable [{}]. Status: {}", feedUrl, response.statusCode());
                return;
            }

            try (InputStream stream = response.body()) {
                SyndFeedInput input = new SyndFeedInput();
                SyndFeed feed = input.build(new InputSource(stream));

                log.info("Feed read: {} ({} articles found)", feed.getTitle(), feed.getEntries().size());

                for (SyndEntry entry : feed.getEntries()) {
                    processArticle(feed, entry);
                }
            }

        } catch (InterruptedException e) {
            log.error("RSS retrieval thread was interrupted for {}", feedUrl);
            Thread.currentThread().interrupt();
        } catch (IOException e) {
            log.error("Network or I/O error while reading feed {}: {}", feedUrl, e.getMessage());
        } catch (Exception e) {
            log.error("Unexpected error while processing feed {}:", feedUrl, e);
        }
    }

    private void processArticle(SyndFeed feed, SyndEntry entry) {
        if (entry.getLink() == null) return;

        Optional<Article> existingArticleOpt = articleRepository.findByLink(entry.getLink());

        if (existingArticleOpt.isEmpty()) {
            // L'article n'existe pas (Nouveau) -> On le crée et on lance le traitement
            String description = (entry.getDescription() != null) ? entry.getDescription().getValue() : "";
            LocalDateTime pubDate = resolvePublicationDate(entry);

            Article newArticle = Article.builder()
                    .title(entry.getTitle())
                    .description(description)
                    .link(entry.getLink())
                    .sourceName(feed.getTitle())
                    .pubDate(pubDate)
                    .build();

            articleRepository.save(newArticle);
            log.info("New article saved: {}. Triggering AI processing...", newArticle.getTitle());
            pythonClient.triggerEnrichment(newArticle.getId());

        } else {
            // L'article existe déjà. On ne fait rien.
            // Si son contenu est vide (erreur Python), le ResilienceService s'en chargera plus tard.
            log.debug("Article already exists in DB: {}", entry.getTitle());
        }
    }

    private LocalDateTime resolvePublicationDate(SyndEntry entry) {
        Date date = entry.getPublishedDate();
        if (date == null) {
            date = entry.getUpdatedDate();
        }
        if (date != null) {
            return date.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
        }
        return LocalDateTime.now();
    }

    @Scheduled(initialDelay = 2000, fixedRate = 3600000)
    public void scheduleFeedUpdate() {
        log.info("Starting automatic RSS scan...");
        fetchRssFeed("https://www.lemondeinformatique.fr/flux-rss/thematique/toute-l-actualite/rss.xml");
    }
}