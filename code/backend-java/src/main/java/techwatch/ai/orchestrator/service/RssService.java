package techwatch.ai.orchestrator.service;

import com.rometools.rome.feed.synd.SyndEntry;
import com.rometools.rome.feed.synd.SyndFeed;
import com.rometools.rome.io.SyndFeedInput;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
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
import java.time.ZoneId;

@Slf4j
@Service
@RequiredArgsConstructor
public class RssService {

    private final ArticleRepository articleRepository;

    // Injection de la valeur configurée dans le YAML
    // Note : On utilise une valeur par défaut "TechWatch-AI/1.0" au cas où la prop serait manquante
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
                    .header("User-Agent", userAgent) // Utilisation de la variable injectée
                    .GET()
                    .build();

            HttpResponse<InputStream> response = HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofInputStream());

            if (response.statusCode() != 200) {
                log.warn("Flux inaccessible [{}]. Status: {}", feedUrl, response.statusCode());
                return;
            }

            try (InputStream stream = response.body()) {
                SyndFeedInput input = new SyndFeedInput();
                SyndFeed feed = input.build(new InputSource(stream));

                log.info("Flux lu : {} ({} articles)", feed.getTitle(), feed.getEntries().size());

                for (SyndEntry entry : feed.getEntries()) {
                    saveArticleIfNotExists(feed, entry);
                }
            }

        } catch (InterruptedException e) {
            log.error("Le thread de récupération RSS a été interrompu pour {}", feedUrl);
            Thread.currentThread().interrupt();
        } catch (IOException e) {
            log.error("Erreur réseau ou E/S lors de la lecture du flux {}: {}", feedUrl, e.getMessage());
        } catch (Exception e) {
            log.error("Erreur inattendue lors du traitement du flux {}:", feedUrl, e);
        }
    }

    private void saveArticleIfNotExists(SyndFeed feed, SyndEntry entry) {
        if (entry.getLink() == null) return;

        if (articleRepository.findByLink(entry.getLink()).isEmpty()) {
            String description = (entry.getDescription() != null) ? entry.getDescription().getValue() : "";

            Article article = Article.builder()
                    .title(entry.getTitle())
                    .description(description)
                    .link(entry.getLink())
                    .sourceName(feed.getTitle())
                    .pubDate(entry.getPublishedDate() != null ?
                            entry.getPublishedDate().toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime() : null)
                    .build();

            articleRepository.save(article);
            log.debug("Article sauvegardé : {}", article.getTitle());
        }
    }
}