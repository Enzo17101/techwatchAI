package techwatch.ai.orchestrator.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Represents an article retrieved via an RSS feed or a website.
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

    // The URL is unique to avoid duplicates during successive scans
    @Column(unique = true, nullable = false, length = 1024)
    private String link;

    private String sourceName;

    private LocalDateTime pubDate;

    // Field for the full content once scraped by the Python service
    @Column(columnDefinition = "TEXT")
    private String fullContent;

    // Audit: allows knowing when the entry was created in the database
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}