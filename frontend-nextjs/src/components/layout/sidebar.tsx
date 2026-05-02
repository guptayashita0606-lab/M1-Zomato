"use client";

import { useState } from "react";

interface SidebarProps {
  currentPage?: string;
}

export function Sidebar({ currentPage = "recommendations" }: SidebarProps) {
  const menuItems = [
    {
      id: "intelligence",
      icon: "psychology",
      label: "Intelligence Hub",
      active: false,
    },
    {
      id: "recommendations",
      icon: "auto_awesome",
      label: "Recommendation Feed",
      active: currentPage === "recommendations",
    },
    {
      id: "chat",
      icon: "chat_bubble",
      label: "Chat Assistant",
      active: false,
    },
    {
      id: "insights",
      icon: "analytics",
      label: "Recent Insights",
      active: false,
    },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full flex flex-col p-6 z-40 bg-white h-screen w-72 rounded-r-lg border-r border-red-50 shadow-lg">
      <div className="mb-8 flex items-center gap-2">
        <span className="text-xl font-bold text-[#b7122a]" style={{ fontFamily: 'Epilogue, sans-serif' }}>
          Zomato AI
        </span>
      </div>
      
      <div className="flex flex-col gap-2 flex-1">
        {menuItems.map((item) => (
          <a
            key={item.id}
            className={`flex items-center gap-3 px-6 py-3 rounded-full transition-all duration-300 ${
              item.active
                ? "bg-[#b7122a] text-white shadow-lg"
                : "text-gray-600 hover:bg-red-50"
            }`}
            href="#"
          >
            <span className="material-symbols-outlined">{item.icon}</span>
            <span className="font-semibold tracking-tight" style={{ fontFamily: 'Epilogue, sans-serif' }}>
              {item.label}
            </span>
          </a>
        ))}
      </div>
      
      <div className="mt-auto pt-8 border-t border-red-50">
        <div className="flex items-center gap-4 p-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#b7122a] to-[#db313f] flex items-center justify-center">
            <span className="material-symbols-outlined text-white text-sm">person</span>
          </div>
          <div>
            <p className="text-sm font-semibold" style={{ fontFamily: 'Epilogue, sans-serif' }}>
              Culinary Joy
            </p>
            <p className="text-xs text-gray-600" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
              AI Recommendation Engine
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
