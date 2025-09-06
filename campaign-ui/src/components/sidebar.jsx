// src/components/Sidebar.jsx
import React from "react";

export function Sidebar() {
  return (
    <aside className="hidden lg:block w-72 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto p-4 space-y-6">
      <section>
        <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">
          Brands
        </h2>
        <ul className="space-y-1">
          <li>
            <button className="block w-full text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              All Brands
            </button>
          </li>
          <li>
            <button className="block w-full text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              EnduraStride
            </button>
          </li>
          <li>
            <button className="block w-full text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              SprintStyle
            </button>
          </li>
        </ul>
      </section>
      <section>
        <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-2">
          Trending USPs
        </h2>
        <ul className="space-y-1">
          <li>
            <button className="block w-full text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              #TripleGuard
            </button>
          </li>
          <li>
            <button className="block w-full text-left px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              #StyleYourRun
            </button>
          </li>
        </ul>
      </section>
    </aside>
  );
}