package techwatch.ai.orchestrator.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Représente un article récupéré via un flux RSS ou un site web.
 */
@Entity
@Table(name = "articles")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Article {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    // L'URL est unique pour éviter les doublons lors des scans successifs
    @Column(unique = true, nullable = false, length = 1024)
    private String link;

    private String sourceName;

    private LocalDateTime pubDate;

    // Champ pour le contenu complet une fois scrappé par le service Python
    @Column(columnDefinition = "TEXT")
    private String fullContent;

    // Audit : permet de savoir quand l'entrée a été créée en base
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}