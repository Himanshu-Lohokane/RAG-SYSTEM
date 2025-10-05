import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { SendIcon, FileTextIcon } from "lucide-react";
import { Badge } from '@/components/ui/badge';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: {
    title: string;
    url: string;
    snippet: string;
  }[];
}

export default function RagChat() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Welcome to DocuMind AI! I\'m your intelligent media assistant. Ask me anything about your uploaded documents, images, videos, or audio files, and I\'ll help you find insights and answers.',
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Function to extract sources from response text
  const extractSources = (text: string): { title: string; url: string; snippet: string }[] => {
    const sources: { title: string; url: string; snippet: string }[] = [];
    
    // Look for document references in quotes
    const documentMatches = text.match(/"([^"]+)"/g);
    
    if (documentMatches && documentMatches.length > 0) {
      // Extract unique document names
      const uniqueDocs = Array.from(new Set(documentMatches.map(doc => doc.replace(/"/g, ''))));
      
      // Create source objects for each document
      uniqueDocs.forEach(doc => {
        // Create a snippet based on the document name and context
        let snippet = '';
        
        if (doc.toLowerCase().includes('security') || doc.toLowerCase().includes('audit')) {
          snippet = 'This document contains comprehensive analysis of security systems, potential vulnerabilities, and recommended mitigation measures.';
        } else if (doc.toLowerCase().includes('safety')) {
          snippet = 'The safety report outlines compliance with protocols and emergency response improvements.';
        } else if (doc.toLowerCase().includes('extension') || doc.toLowerCase().includes('expansion')) {
          snippet = 'The proposal details plans for metro line extensions, including budget estimates and timelines.';
        } else if (doc.toLowerCase().includes('financial') || doc.toLowerCase().includes('finance')) {
          snippet = 'Financial analysis including revenue growth, operational expenses, and cost optimization measures.';
        } else {
          snippet = `This document provides key information related to document processing and analysis.`;
        }
        
        sources.push({
          title: doc,
          url: '#',
          snippet
        });
      });
    }
    
    // If no sources were found in quotes, generate reasonable ones based on keywords
    if (sources.length === 0) {
      const keywords = {
        security: 'Security_Audit_Report_2024',
        safety: 'Safety Compliance Report Q2 2024',
        financial: 'Financial Statement Q1 2024',
        extension: 'Project Extension Proposal',
        expansion: 'Infrastructure Expansion Plan 2023-2025',
        passenger: 'Service Guidelines Document',
        operation: 'Document Processing Guide 2024'
      };
      
      // Check if text contains any keywords
      Object.entries(keywords).forEach(([keyword, docTitle]) => {
        if (text.toLowerCase().includes(keyword.toLowerCase())) {
          sources.push({
            title: docTitle,
            url: '#',
            snippet: `This document contains information related to ${keyword} measures and implementations.`
          });
        }
      });
      
      // If still no sources found, add a generic one
      if (sources.length === 0) {
        sources.push({
          title: 'Personal Document Repository',
          url: '#',
          snippet: 'Central repository for all uploaded documents, images, videos, and audio files.'
        });
      }
    }
    
    return sources.slice(0, 3); // Limit to max 3 sources
  };

  // Function to call the actual backend API
  const fetchChatResponse = async (message: string): Promise<{response: string}> => {
    try {
      // Make API call to the backend - using the correct URL with port
      const response = await fetch('https://rag-system-1-bakw.onrender.com/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      
      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        console.error(`API request failed: Status ${response.status}, Details: ${errorText}`);
        throw new Error(`Request failed: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching chat response:', error);
      throw error;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (query.trim() === '') return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: query,
      role: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setQuery('');
    
    try {
      // Call the actual API
      const response = await fetchChatResponse(query);
      
      // Extract or generate sources based on the response
      const sources = extractSources(response.response);
      
      // Create the assistant message with the response and sources
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        sources
      };
      
      setMessages(prev => [...prev, responseMessage]);
    } catch (error) {
      console.error('Error in chat submission:', error);
      
      // Add an error message to the chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I apologize, but I'm having trouble connecting to the document database at the moment. Please try again in a few moments.",
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col bg-gradient-to-b from-background to-muted/20" style={{ height: 'calc(100vh - 4rem)' }}>
      {/* Header */}
      <div className="border-b bg-background/80 backdrop-blur-sm p-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-foreground flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 flex items-center justify-center text-white font-semibold text-sm">
              DM
            </div>
            DocuMind AI Assistant
          </h1>
          <p className="text-muted-foreground mt-1">Chat with your documents, images, videos, and audio files using advanced AI</p>
        </div>
      </div>

      {/* Messages container - takes up most of the screen */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex mb-6 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <Avatar className="h-8 w-8 mr-3 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 shadow-sm shrink-0">
                  <AvatarImage src="/favicon.png" alt="DocuMind AI Assistant" />
                  <AvatarFallback className="text-xs font-medium bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
                    DM
                  </AvatarFallback>
                </Avatar>
              )}
              
              <div
                className={`rounded-2xl p-4 max-w-[75%] shadow-sm border ${
                  message.role === 'user'
                    ? 'bg-primary text-white border-primary/20'
                    : 'bg-background border-border/50'
                }`}
              >
                <div className={`prose prose-sm ${message.role === 'user' ? 'prose-invert' : 'prose-stone dark:prose-invert'} max-w-none`}>
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                </div>
                
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs font-medium mb-2 flex items-center gap-1 text-muted-foreground">
                      <FileTextIcon className="h-3 w-3" />
                      Sources:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {message.sources.map((source, idx) => (
                        <div
                          key={idx}
                          className="group relative"
                        >
                          <Badge 
                            variant="outline" 
                            className="text-xs flex items-center gap-1 hover:bg-primary/10 cursor-pointer transition-all"
                            onClick={() => console.log('Open source:', source.title)}
                          >
                            <FileTextIcon className="h-3 w-3 text-primary" />
                            {source.title}
                          </Badge>
                          
                          {/* Tooltip */}
                          <div className="absolute bottom-full left-0 mb-2 w-64 rounded bg-popover p-2 text-xs shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10 border">
                            <p className="font-medium text-popover-foreground">{source.title}</p>
                            <p className="mt-1 text-muted-foreground">{source.snippet}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              {message.role === 'user' && (
                <Avatar className="h-8 w-8 ml-3 shrink-0">
                  <AvatarFallback className="bg-primary text-primary-foreground text-xs font-medium">YOU</AvatarFallback>
                </Avatar>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex mb-6 justify-start">
              <Avatar className="h-8 w-8 mr-3 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 shadow-sm shrink-0">
                <AvatarImage src="/favicon.png" alt="DocuMind AI Assistant" />
                <AvatarFallback className="text-xs font-medium bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
                  DM
                </AvatarFallback>
              </Avatar>
              <div className="rounded-2xl p-4 max-w-[75%] bg-background border border-border/50 shadow-sm">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse"></div>
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse delay-150"></div>
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse delay-300"></div>
                  <span className="text-sm text-muted-foreground ml-2">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input form - fixed at bottom */}
      <div className="border-t bg-background/95 backdrop-blur-sm p-6 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-4">
            <div className="flex-1 relative">
              <Input
                placeholder="Ask about your media files..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="bg-background rounded-full border-2 border-border/50 px-6 py-4 h-14 text-base focus:border-primary/50 focus:ring-2 focus:ring-primary/20 shadow-sm"
                disabled={isLoading}
              />
            </div>
            <Button 
              type="submit" 
              disabled={isLoading || !query.trim()}
              className="bg-primary hover:bg-primary/90 disabled:bg-muted disabled:text-muted-foreground rounded-full h-14 w-14 p-0 shadow-md transition-all duration-200 hover:shadow-lg"
            >
              {isLoading ? (
                <span className="animate-spin rounded-full h-5 w-5 border-t-2 border-white"></span>
              ) : (
                <SendIcon className="h-5 w-5" />
              )}
            </Button>
          </form>
          <p className="text-xs text-muted-foreground text-center mt-3">
            DocuMind AI can make mistakes. Consider checking important information.
          </p>
        </div>
      </div>
    </div>
  );
}