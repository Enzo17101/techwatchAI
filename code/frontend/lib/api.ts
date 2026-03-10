import axios from 'axios';

// On définit l'URL de base de notre Orchestrateur Java
// En développement, c'est localhost:8080
// En prod, ce sera une variable d'environnement
const JAVA_API_URL = process.env.NEXT_PUBLIC_JAVA_API_URL || 'http://localhost:8080/api';

/**
 * Instance Axios configurée pour parler au Backend Java.
 * Avantages :
 * 1. Pas besoin de répéter l'URL de base à chaque appel.
 * 2. On peut intercepter les erreurs globalement (ex: afficher une notif si le serveur est down).
 * 3. Gestion automatique des headers JSON.
 */
export const apiClient = axios.create({
  baseURL: JAVA_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Timeout de 10s pour ne pas bloquer l'interface indéfiniment
  timeout: 10000,
});

// Type Definition pour nos Articles (DTO Frontend)
// C'est le miroir exact de ton ArticleResponseDTO Java !
export interface Article {
  id: string;
  title: string;
  description: string;
  link: string;
  sourceName: string;
  pubDate: string; // Les dates arrivent en String (ISO) du JSON
}

// Service pour récupérer les articles
export const ArticleService = {
  getAll: async (page = 0, size = 10) => {
    try {
      // Appel vers Java : GET /articles?page=0&size=10
      const response = await apiClient.get(`/articles?page=${page}&size=${size}`);
      return response.data; // Retourne l'objet Page<ArticleResponseDTO>
    } catch (error) {
      console.error('Erreur lors de la récupération des articles:', error);
      throw error;
    }
  }
};