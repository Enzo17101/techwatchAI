import requests
import logging

logger = logging.getLogger(__name__)

class AiService:
    def __init__(self):
        # TODO: Consider extracting these values to environment variables for production
        self.ollama_base_url = "http://localhost:11434/api"
        self.embedding_model = "nomic-embed-text"
        self.chat_model = "qwen3:8b"

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a mathematical vector (embedding) from the provided text.
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
            return result_data.get("embedding", [])

        except Exception as e:
            logger.error("Failed to generate vector embedding: %s", e)
            raise e

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generates an answer using the provided context (RAG).
        Uses advanced prompt engineering with XML tags to enforce context usage,
        while allowing a fallback to general knowledge if necessary.
        """
        try:

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
            """

            # prompt = f"""You are a technology watch expert AI named "TechWatch".
            
            # Here are the excerpts from recent articles retrieved from our database:
            
            # <context>
            # {context}
            # </context>

            # STRICT INSTRUCTIONS:
            # 1. Carefully read the articles provided in the <context> tag.
            # 2. Your absolute mission is to answer the user's question USING THIS <context>.
            # 3. If the information in the <context> allows you to answer (even partially or phrased differently), you MUST formulate your answer based on this information.
            # 4. ONLY IF the <context> contains absolutely no information related to the topic of the question, you may use your general knowledge, but you MUST strictly start your sentence with: "Recent articles do not mention this specific point, but based on my general knowledge..."
            # 5. Always answer in a clear, concise, and professional manner.

            # User question: {question}
            # """

            payload = {
                "model": self.chat_model,
                "prompt": prompt,
                "stream": False
            }

            logger.info("Requesting answer from Ollama model (%s)...", self.chat_model)
            
            response = requests.post(f"{self.ollama_base_url}/generate", json=payload, timeout=120)
            response.raise_for_status()

            result_data = response.json()
            answer = result_data.get("response", "")

            return answer.strip()

        except Exception as e:
            logger.error("Failed to generate answer: %s", e)
            raise e

    def generate_answer_strict(self, question: str, context: str) -> str:
        """
        Generates an answer using strict RAG rules.
        Fallback to general knowledge is strictly forbidden.
        """
        try:

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

            # prompt = f"""You are the TechWatch AI assistant.
            # Your role is to answer the user's question accurately and professionally.
            
            # IMPORTANT: You must ONLY use the information contained in the CONTEXT below.
            # If the answer is not found in the context, simply say "I could not find any information about this in recent watch articles." Do not invent answers.
    
            # ARTICLE CONTEXT:
            # ---------------------
            # {context}
            # ---------------------
    
            # USER QUESTION: {question}
            # """

            payload = {
                "model": self.chat_model,
                "prompt": prompt,
                "stream": False
            }

            logger.info("Requesting strict answer from Ollama model (%s)...", self.chat_model)

            response = requests.post(f"{self.ollama_base_url}/generate", json=payload, timeout=120)
            response.raise_for_status()

            result_data = response.json()
            answer = result_data.get("response", "")

            return answer.strip()

        except Exception as e:
            logger.error("Failed to generate strict answer: %s", e)
            raise e