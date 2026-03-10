"use client";

import React from 'react';
import { Search, RefreshCw } from 'lucide-react';

interface HeaderProps {
  activeView: 'feed' | 'chat';
}

export function Header({ activeView }: HeaderProps) {
  return (
    <header className="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-8 shrink-0">
      <div className="flex items-center gap-3">
        <h2 className="font-bold text-slate-800 dark:text-slate-100">
          {activeView === 'feed' ? 'Monitoring Feed' : 'AI Assistant'}
        </h2>
        <div className="h-4 w-[1px] bg-slate-300 dark:bg-slate-700" />
        <span className="text-xs text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-full font-medium tracking-wide">
          BETA
        </span>
      </div>
      
      <div className="flex items-center gap-4">
        {/* Search bar placeholder - Functional implementation would require a dedicated state */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={14} />
          <input 
            className="pl-9 pr-4 py-1.5 bg-slate-100 dark:bg-slate-800 border-none rounded-lg text-sm w-64 focus:ring-2 focus:ring-blue-500/20 focus:outline-none dark:text-white transition-all" 
            placeholder="Search articles..." 
          />
        </div>
        
        <button 
          onClick={() => window.location.reload()}
          className="p-2 text-slate-400 hover:text-blue-600 transition-colors"
          title="Refresh application"
        >
          <RefreshCw size={18} />
        </button>
      </div>
    </header>
  );
}