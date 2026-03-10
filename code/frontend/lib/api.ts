import axios from 'axios';

// Java Orchestrator base URL configuration
const JAVA_API_URL = process.env.NEXT_PUBLIC_JAVA_API_URL || 'http://localhost:8080/api';

/**
 * Global Axios instance configured for backend communication.
 * Centralizes base URL, headers, and timeout settings.
 */
export const apiClient = axios.create({
  baseURL: JAVA_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Article data structure representing the metadata retrieved from the orchestrator.
 * Matches the ArticleResponseDTO from the Spring Boot backend.
 */
export interface Article {
  id: string;
  title: string;
  description: string;
  link: string;
  sourceName: string;
  pubDate: string; // ISO format
}

/**
 * Service handling article-related API interactions.
 */
export const ArticleService = {
  /**
   * Retrieves a paginated list of articles.
   * @param page - Current page index
   * @param size - Number of elements per page
   */
  getAll: async (page = 0, size = 10) => {
    try {
      const response = await apiClient.get('/articles', {
        params: { page, size }
      });
      return response.data;
    } catch (error) {
      console.error('API Error: Failed to fetch articles:', error);
      throw error;
    }
  }
};