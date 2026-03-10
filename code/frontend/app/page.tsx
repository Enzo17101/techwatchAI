"use client";

import React, { useState, useEffect } from 'react';
import { Article, ArticleService } from '@/lib/api';
import { Sidebar } from '@/components/layout/sidebar';
import { Header } from '@/components/layout/header';
import { ArticleGrid } from '@/components/article/article-grid';
import { ChatInterface } from '@/components/chat/chat-panel';

type ViewMode = 'feed' | 'chat';

export default function Home() {
  const [activeView, setActiveView] = useState<ViewMode>('feed');
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function fetchArticles() {
      try {
        setLoading(true);
        // Connect to the Java-based orchestrator API
        const response = await ArticleService.getAll(0, 12);
        setArticles(response.content || []);
        setError(false);
      } catch (e) {
        console.error("Failed to fetch monitoring articles:", e);
        setError(true);
      } finally {
        setLoading(false);
      }
    }
    fetchArticles();
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 overflow-hidden font-sans">
      
      <Sidebar activeView={activeView} setActiveView={setActiveView} />

      <div className="flex-1 flex flex-col min-w-0">
        <Header activeView={activeView} />

        <main className="flex-1 overflow-y-auto bg-slate-50/50 dark:bg-slate-950">
          {activeView === 'feed' ? (
            <div className="max-w-7xl mx-auto p-8">
              <div className="mb-8">
                <h1 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight uppercase">
                  Latest Updates
                </h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">
                  Technical sources analyzed and vectorized in real-time.
                </p>
              </div>
              <ArticleGrid articles={articles} loading={loading} error={error} />
            </div>
          ) : (
            <div className="pt-8 h-full">
              <ChatInterface />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}