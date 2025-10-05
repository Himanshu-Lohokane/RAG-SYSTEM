import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'DocuMind AI - Intelligent Document Processing',
  description: 'Personal multi-modal AI agent for intelligent document processing, OCR, and knowledge extraction',
  keywords: 'AI document processing, OCR, multi-modal AI, RAG, knowledge extraction, personal AI assistant',
  authors: [{ name: 'DocuMind AI' }],
  openGraph: {
    title: 'DocuMind AI - Intelligent Document Processing',
    description: 'Personal multi-modal AI agent for intelligent document processing and knowledge extraction',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className} suppressHydrationWarning={true}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          {children}
        </TooltipProvider>
      </body>
    </html>
  )
}
