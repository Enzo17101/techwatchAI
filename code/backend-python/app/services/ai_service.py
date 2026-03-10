import requests
import logging

logger = logging.getLogger(__name__)

class AiService:
    def __init__(self):
        # Configuration des modèles Ollama
        self.ollama_base_url = "http://localhost:11434/api"
        # Modèle pour les vecteurs (Petit et rapide)
        self.embedding_model = "nomic-embed-text"
        # Modèle de discussion
        self.chat_model = "qwen3:8b"

    def generate_embedding(self, text: str) -> list[float]:
        """
        Génère un vecteur mathématique à partir d'un texte.
        (C'est la méthode que nous avons codée précédemment).
        """
        try:
            if not text or len(text.strip()) == 0:
                return []

            clean_text = text.replace("\n", " ")

            payload = {
                "model": self.embedding_model,
                "prompt": clean_text
            }

            response = requests.post(f"{self.ollama_base_url}/embeddings", json=payload, timeout=60)
            response.raise_for_status()

            result_data = response.json()
            vector = result_data.get("embedding", [])

            return vector

        except Exception as e:
            logger.error(f"Erreur lors de la génération du vecteur: {e}")
            raise e

    def generate_answer(self, question: str, context: str) -> str:
        """
        Demande à l'IA de répondre à la question en utilisant le contexte fourni.
        C'est le cœur du RAG !
        """
        try:
            # Le "Prompt System" : On donne des ordres stricts à l'IA
            prompt = f"""Tu es un expert en analyse de veille technologique nommé "TechWatch".
            
            Voici les extraits d'articles récents récupérés dans notre base de données :
            
            <context>
            {context}
            </context>

            INSTRUCTIONS STRICTES :
            1. Lis attentivement les articles fournis dans la balise <context>.
            2. Ta mission absolue est de répondre à la question de l'utilisateur EN UTILISANT CE <context>.
            3. Si les informations dans le <context> permettent de répondre (même partiellement ou formulées différemment), tu DOIS formuler ta réponse à partir de ces informations.
            4. UNIQUEMENT SI le <context> ne contient absolument aucune information liée au sujet de la question, tu peux utiliser tes connaissances, mais tu DOIS obligatoirement commencer ta phrase EXACTEMENT par : "Les articles récents ne mentionnent pas ce point précis, mais d'après mes connaissances générales..."
            5. Réponds toujours en français, de manière claire, concise et professionnelle.

            Question de l'utilisateur : {question}
            
            Ta réponse :
            """

            payload = {
                "model": self.chat_model,
                "prompt": prompt,
                "stream": False # Pour l'instant on attend la réponse complète (plus simple à débugger)
            }

            logger.info(f"Demande de réponse à Ollama ({self.chat_model})...")

            # Timeout plus long car le LLM doit lire tout le contexte et réfléchir
            response = requests.post(f"{self.ollama_base_url}/generate", json=payload, timeout=120)
            response.raise_for_status()

            result_data = response.json()
            answer = result_data.get("response", "")

            return answer

        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse: {e}")
            raise e

    def generate_answer_strict(self, question: str, context: str) -> str:
        """
        Demande à l'IA de répondre à la question en utilisant le contexte fourni.
        C'est le cœur du RAG !
        """
        try:
            # Le "Prompt System" : On donne des ordres stricts à l'IA
            prompt = f"""Tu es l'assistant IA de veille technologique "TechWatch".
            Ton rôle est de répondre à la question de l'utilisateur de manière précise et professionnelle.
            
            IMPORTANT : Tu dois utiliser UNIQUEMENT les informations contenues dans le CONTEXTE ci-dessous.
            Si la réponse ne se trouve pas dans le contexte, dis simplement "Je n'ai pas trouvé d'information à ce sujet dans les articles récents de la veille." Ne t'invente pas de réponses.
            Réponds toujours en français.
    
            CONTEXTE DES ARTICLES :
            ---------------------
            {context}
            ---------------------
    
            QUESTION DE L'UTILISATEUR : {question}
            """

            payload = {
                "model": self.chat_model,
                "prompt": prompt,
                "stream": False # Pour l'instant on attend la réponse complète (plus simple à débugger)
            }

            logger.info(f"Demande de réponse à Ollama ({self.chat_model})...")

            # Timeout plus long car le LLM doit lire tout le contexte et réfléchir
            response = requests.post(f"{self.ollama_base_url}/generate", json=payload, timeout=120)
            response.raise_for_status()

            result_data = response.json()
            answer = result_data.get("response", "")

            return answer

        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse: {e}")
            raise e