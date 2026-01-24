package techwatch.ai.orchestrator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import techwatch.ai.orchestrator.entity.Article;
import java.util.UUID;
import java.util.Optional;

@Repository
public interface ArticleRepository extends JpaRepository<Article, UUID> {
    // Méthode pratique pour vérifier si on a déjà traité ce lien
    Optional<Article> findByLink(String link);
}