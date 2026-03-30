# ÉTAPE 1 : Build (Compilation)
# On utilise une image officielle Maven avec le JDK 21
FROM maven:3.9.6-eclipse-temurin-21 AS builder

# On définit le répertoire de travail dans le conteneur
WORKDIR /build

# On copie le fichier pom.xml et on télécharge les dépendances
# Cette étape est mise en cache par Docker pour accélérer les futurs builds
COPY pom.xml .
RUN mvn dependency:go-offline

# On copie le code source
COPY src ./src

# On compile l'application en ignorant les tests pour aller plus vite lors du build Docker
RUN mvn clean package -DskipTests

# ÉTAPE 2 : Run (Exécution)
# On utilise une image beaucoup plus légère contenant uniquement le JRE (Java Runtime Environment)
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# On crée un utilisateur non-root pour des raisons de sécurité (bonne pratique de production)
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# On récupère le fichier .jar généré à l'étape 1 (builder)
COPY --from=builder /build/target/*.jar app.jar

# On expose le port sur lequel Spring Boot écoute par défaut
EXPOSE 8080

# Commande de démarrage de l'application
ENTRYPOINT ["java", "-jar", "app.jar"]