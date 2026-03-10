"use client";

import React from 'react';
import { LayoutDashboard, MessageSquare, Settings, Bot } from 'lucide-react';

interface SidebarProps {
  activeView: 'feed' | 'chat';
  setActiveView: (view: 'feed' | 'chat') => void;
}

export function Sidebar({ activeView, setActiveView }: SidebarProps) {
  return (
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col h-full shrink-0">
      <div className="p-6 flex items-center gap-3">
        <div className="bg-blue-600 p-2 rounded-lg text-white">
          <Bot size={20} />
        </div>
        <span className="font-bold text-lg tracking-tight">TechWatch AI</span>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        <button 
          onClick={() => setActiveView('feed')}
          className={`flex items-center gap-3 w-full px-4 py-2.5 rounded-lg transition-all text-sm font-medium ${
            activeView === 'feed' 
              ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' 
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
          }`}
        >
          <LayoutDashboard size={18} /> Actualités
        </button>
        <button 
          onClick={() => setActiveView('chat')}
          className={`flex items-center gap-3 w-full px-4 py-2.5 rounded-lg transition-all text-sm font-medium ${
            activeView === 'chat' 
              ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' 
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
          }`}
        >
          <MessageSquare size={18} /> Assistant IA
        </button>
      </nav>

      <div className="p-4 mt-auto border-t border-slate-100 dark:border-slate-800">
        <button className="flex items-center gap-3 w-full px-4 py-2 text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-colors text-sm font-medium">
          <Settings size={18} /> Paramètres
        </button>
      </div>
    </aside>
  );
}