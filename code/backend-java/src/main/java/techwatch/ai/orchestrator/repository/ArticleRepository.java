package techwatch.ai.orchestrator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import techwatch.ai.orchestrator.entity.Article;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ArticleRepository extends JpaRepository<Article, UUID> {

    Optional<Article> findByLink(String link);

    /**
     * Retrieves a batch of articles that haven't been fully scraped yet.
     * Limited to 50 to prevent downstream processing bottlenecks.
     */
    @Query(value = "SELECT * FROM articles WHERE full_content IS NULL OR full_content = '' LIMIT 50", nativeQuery = true)
    List<Article> findIncompleteArticles();
}