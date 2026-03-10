from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.services.ai_service import AiService

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AiService()
        self.content_size = 4000

    def search_and_answer(self, question: str) -> str:
        """
        Le pipeline complet du RAG (Retrieval-Augmented Generation)
        """
        logger.info(f"RAG: Nouvelle question reçue -> '{question}'")

        # 1. RETRIEVAL : Transformer la question en vecteur (Embedding)
        logger.info("RAG: Génération du vecteur pour la question...")
        question_vector = self.ai_service.generate_embedding(question)

        if not question_vector:
            return "Désolé, je n'ai pas pu comprendre votre question."

        # Convertir la liste de float en string pour la requête SQL pgvector
        # Format attendu par pgvector : '[0.1, 0.2, -0.5, ...]'
        vector_str = f"[{','.join(map(str, question_vector))}]"

        # 2. RETRIEVAL : Chercher les 3 articles les plus proches dans la base de données
        # On utilise l'opérateur `<->` de pgvector qui calcule la distance cosinus (L2 distance)
        # On ne prend que les articles qui ont un vecteur (embedding IS NOT NULL)
        logger.info("RAG: Recherche des articles similaires dans PostgreSQL (pgvector)...")

        query = text("""
            SELECT title, source_name, full_content 
            FROM articles 
            WHERE embedding IS NOT NULL 
            ORDER BY embedding <-> :vector 
            LIMIT 3
        """)

        results = self.db.execute(query, {"vector": vector_str}).fetchall()

        if not results:
            logger.warning("RAG: Aucun article avec vecteur trouvé dans la base.")
            return "Désolé, ma base de données d'articles semble vide ou en cours d'indexation. Veuillez réessayer plus tard."

        # 3. AUGMENTATION : Préparer le contexte
        logger.info(f"RAG: {len(results)} articles pertinents trouvés. Préparation du contexte.")
        context = ""
        for row in results:
            title = row[0]
            source = row[1]
            content = row[2]
            print("content size : ", len(content))
            print("content : ", content)

            # On tronque le contenu de chaque article pour ne pas exploser la mémoire du LLM
            truncated_content = content[:self.content_size] + "..." if content and len(content) > self.content_size else (content or "")

            context += f"\n--- Article : {title} (Source: {source}) ---\n"
            context += f"{truncated_content}\n"

        # 4. GENERATION : Demander à l'IA de répondre
        logger.info("RAG: Demande de génération de la réponse au LLM...")
        answer = self.ai_service.generate_answer(question, context)

        logger.info("RAG: Réponse générée avec succès.")
        return answer