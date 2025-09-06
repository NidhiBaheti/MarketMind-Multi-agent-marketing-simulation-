// src/components/Header.jsx
import React from "react";
import { Home, Search, Bell, User } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-6xl mx-auto flex items-center justify-between h-16 px-4">
        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
          MarketMind
        </div>
        <nav className="hidden md:flex space-x-6">
          <a
            href="#"
            className="flex items-center text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
          >
            <Home className="w-5 h-5 mr-1" /> Home
          </a>
          <a
            href="#"
            className="flex items-center text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
          >
            <Search className="w-5 h-5 mr-1" /> Explore
          </a>
        </nav>
        <div className="flex items-center space-x-4">
          <button className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
            <Bell className="w-5 h-5" />
          </button>
          <button className="flex items-center text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
            <User className="w-5 h-5 mr-1" /> Profile
          </button>
        </div>
      </div>
    </header>
);
}