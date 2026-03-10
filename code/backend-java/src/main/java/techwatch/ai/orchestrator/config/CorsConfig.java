package techwatch.ai.orchestrator.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**") // Applique cette règle à toutes nos routes API
                .allowedOrigins("http://localhost:3000") // Autorise notre Frontend Next.js
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // Autorise ces actions
                .allowedHeaders("*")
                .allowCredentials(true);
    }
}