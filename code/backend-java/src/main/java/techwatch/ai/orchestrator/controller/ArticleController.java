package techwatch.ai.orchestrator.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import techwatch.ai.orchestrator.dto.ArticleResponseDTO;
import techwatch.ai.orchestrator.entity.Article;
import techwatch.ai.orchestrator.repository.ArticleRepository;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/articles")
@RequiredArgsConstructor
public class ArticleController {

    private final ArticleRepository articleRepository;

    @GetMapping
    public List<ArticleResponseDTO> getAllArticles() {
        return articleRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    private ArticleResponseDTO convertToDTO(Article article) {
        return ArticleResponseDTO.builder()
                .id(article.getId())
                .title(article.getTitle())
                .description(article.getDescription())
                .link(article.getLink())
                .sourceName(article.getSourceName())
                .pubDate(article.getPubDate())
                .build();
    }
}