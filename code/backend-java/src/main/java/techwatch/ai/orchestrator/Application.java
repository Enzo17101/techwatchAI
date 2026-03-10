package techwatch.ai.orchestrator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync; // <--- Import
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
@EnableAsync // <--- Activation du support asynchrone
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}