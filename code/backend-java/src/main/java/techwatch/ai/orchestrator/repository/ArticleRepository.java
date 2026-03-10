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

    // NOUVEAU : Trouve les articles dont le contenu complet n'a pas encore été scrapé.
    // On limite à 50 pour ne pas surcharger Python d'un seul coup s'il y a un gros arriéré.
    @Query(value = "SELECT * FROM articles WHERE full_content IS NULL OR full_content = '' LIMIT 50", nativeQuery = true)
    List<Article> findIncompleteArticles();
}