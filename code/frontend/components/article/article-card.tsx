import React from 'react';
import { Calendar, ExternalLink } from 'lucide-react';
import { Article } from '@/lib/api';

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  const formattedDate = new Date(article.pubDate).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'short', year: 'numeric'
  });

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full group">
      <div className="p-5 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-4">
          <span className="bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-md">
            {article.sourceName || "Source"}
          </span>
          <span className="text-slate-400 dark:text-slate-500 text-xs flex items-center gap-1.5 font-medium">
            <Calendar size={12} /> {formattedDate}
          </span>
        </div>
        
        {/* CORRECTION : Utilisation de dangerouslySetInnerHTML pour décoder les entités HTML du titre */}
        <h3 
          className="font-bold text-slate-900 dark:text-slate-100 leading-snug mb-3 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors"
          dangerouslySetInnerHTML={{ __html: article.title }}
        />
        
        {/* CORRECTION : Utilisation de dangerouslySetInnerHTML pour la description et passage en <div> */}
        <div 
          className="text-slate-500 dark:text-slate-400 text-sm line-clamp-3 leading-relaxed"
          dangerouslySetInnerHTML={{ __html: article.description || "Aucun résumé fourni par la source." }}
        />
        
      </div>
      <div className="p-5 pt-0 mt-auto border-t border-slate-50 dark:border-slate-800/50">
        <a 
          href={article.link} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-blue-600 dark:text-blue-400 text-sm font-semibold flex items-center gap-1.5 hover:gap-2 transition-all mt-4 w-max"
        >
          Lire l'article complet <ExternalLink size={14} />
        </a>
      </div>
    </div>
  );
}