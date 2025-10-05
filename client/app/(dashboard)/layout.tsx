"use client";

import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [queryClient] = useState(() => new QueryClient());
  const pathname = usePathname();
  
  // Check if current page is the AI assistant (search) page
  const isAIAssistantPage = pathname?.endsWith('/search');

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="flex">
          <Sidebar />
          <main className={`flex-1 ${isAIAssistantPage ? 'p-0' : 'p-6'}`}>
            {children}
          </main>
        </div>
      </div>
    </QueryClientProvider>
  );
}
