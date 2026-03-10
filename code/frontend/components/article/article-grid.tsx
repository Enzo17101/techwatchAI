import React from 'react';
import { Loader2, Newspaper } from 'lucide-react';
import { Article } from '@/lib/api';
import { ArticleCard } from './article-card';

interface ArticleGridProps {
  articles: Article[];
  loading: boolean;
  error: boolean;
}

export function ArticleGrid({ articles, loading, error }: ArticleGridProps) {
  // Loading state with a smooth pulse animation
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-4">
        <Loader2 className="animate-spin text-blue-600" size={40} />
        <p className="text-slate-500 font-medium animate-pulse">
          Synchronizing with the monitoring service...
        </p>
      </div>
    );
  }

  // Error handling for backend connectivity issues
  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/50 p-6 rounded-xl">
        <h3 className="text-red-800 dark:text-red-400 font-bold mb-2">Connection Error</h3>
        <p className="text-red-600 dark:text-red-300 text-sm">
          Unable to reach the backend services. Please ensure the server is running and try again.
        </p>
      </div>
    );
  }

  // Empty state when no data is returned
  if (articles.length === 0) {
    return (
      <div className="text-center py-20 bg-slate-50 dark:bg-slate-900 rounded-xl border border-dashed border-slate-200 dark:border-slate-800">
        <Newspaper className="mx-auto text-slate-300 mb-4" size={48} />
        <p className="text-slate-500 font-medium">No articles found in the database.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {articles.map(article => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
}