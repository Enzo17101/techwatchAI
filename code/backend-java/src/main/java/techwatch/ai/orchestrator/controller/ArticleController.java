package techwatch.ai.orchestrator.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import techwatch.ai.orchestrator.dto.ArticleResponseDTO;
import techwatch.ai.orchestrator.entity.Article;
import techwatch.ai.orchestrator.repository.ArticleRepository;

@Slf4j
@RestController
@RequestMapping("/api/articles")
@RequiredArgsConstructor
public class ArticleController {

    private final ArticleRepository articleRepository;

    /**
     * Retrieves a paginated list of articles.
     *
     * @param pageable pagination and sorting parameters
     * @return a paginated list of ArticleResponseDTO
     */
    @GetMapping
    public Page<ArticleResponseDTO> getAllArticles(
            @PageableDefault(size = 10, sort = "pubDate", direction = Sort.Direction.DESC) Pageable pageable
    ) {
        log.debug("Fetching articles - page: {}, size: {}", pageable.getPageNumber(), pageable.getPageSize());

        return articleRepository.findAll(pageable)
                .map(this::convertToDTO);
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