package techwatch.ai.orchestrator.dto;

import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
public class ArticleResponseDTO {
    private UUID id;
    private String title;
    private String description;
    private String link;
    private String sourceName;
    private LocalDateTime pubDate;
}