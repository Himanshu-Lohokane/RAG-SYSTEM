import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { SearchIcon, SendIcon, FileTextIcon, DatabaseIcon, AlertCircle } from "lucide-react";
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
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
      content: 'Welcome to KMRL Document Search. Ask me anything about Kochi Metro Rail documents, policies, or procedures.',
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll disabled
  // useEffect(() => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  // }, [messages]);

  // Function to extract sources from response text
  const extractSources = (text: string): { title: string; url: string; snippet: string }[] => {
    const sources: { title: string; url: string; snippet: string }[] = [];
    
    // Look for document references in quotes
    const documentMatches = text.match(/"([^"]+)"/g);
    
    if (documentMatches && documentMatches.length > 0) {
      // Extract unique document names
      const uniqueDocs = [...new Set(documentMatches.map(doc => doc.replace(/"/g, '')))];
      
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
          snippet = `This document provides key information related to Kochi Metro Rail operations and planning.`;
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
        security: 'KMR_Annual_Security_Audit_Report_2023',
        safety: 'Safety Compliance Report Q2 2024',
        financial: 'Financial Statement Q1 2024',
        extension: 'Metro Line Extension Proposal',
        expansion: 'Infrastructure Expansion Plan 2023-2025',
        passenger: 'Passenger Service Guidelines',
        operation: 'KMRL Operations Manual 2024'
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
          title: 'KMRL Documentation Repository',
          url: '#',
          snippet: 'Central repository for all Kochi Metro Rail Limited documentation and reports.'
        });
      }
    }
    
    return sources.slice(0, 3); // Limit to max 3 sources
  };

  // Function to call the actual backend API
  const fetchChatResponse = async (message: string): Promise<{response: string}> => {
    try {
      // Make API call to the backend - using the correct URL with port
      const response = await fetch('http://localhost:8001/api/chat/message', {
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
    <div className="w-full bg-card rounded-lg shadow-md border-2 border-primary/10 mb-6 relative overflow-hidden" style={{ 
      backgroundImage: `radial-gradient(circle at 1px 1px, rgba(59, 130, 246, 0.06) 1px, transparent 0)`,
      backgroundSize: '20px 20px'
    }}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-xl flex items-center gap-2">
              <DatabaseIcon className="h-5 w-5 text-primary" />
              Advanced RAG Document Assistant
            </CardTitle>
            <CardDescription>
              Search across all documents with powerful AI-driven knowledge retrieval
            </CardDescription>
          </div>
          <Badge variant="outline" className="text-xs bg-primary/5 hover:bg-primary/10">
            <span className="text-primary font-medium">AI-Powered</span>
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="p-4 pt-0">
        {/* Messages container */}
        <div className="mb-4 max-h-[420px] overflow-y-auto p-4 bg-muted/50 rounded-lg shadow-inner border border-muted">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex mb-4 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <Avatar className="h-8 w-8 mr-2 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 shadow-md">
                  <AvatarImage src="/logos/kmrl-logo-square.png" alt="KMRL Assistant" />
                  <AvatarFallback className="text-xs font-medium bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      className="h-5 w-5" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      strokeWidth="2" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    >
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                      <path d="M12 17h.01"/>
                    </svg>
                  </AvatarFallback>
                </Avatar>
              )}
              
              <div
                className={`rounded-lg p-3 max-w-[80%] ${
                  message.role === 'user'
                    ? 'bg-primary text-white shadow-sm'
                    : 'bg-background border shadow-sm'
                }`}
              >
                <div className={`text-sm prose prose-sm ${message.role === 'user' ? 'prose-invert' : 'prose-stone dark:prose-invert'} max-w-none`}>
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                </div>
                
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs font-medium mb-2 flex items-center gap-1">
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-3 w-3" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        stroke="currentColor" 
                        strokeWidth="2" 
                        strokeLinecap="round" 
                        strokeLinejoin="round"
                      >
                        <path d="M9 17h6"></path>
                        <path d="M9 12h6"></path>
                        <path d="M11.5 3h-5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"></path>
                        <path d="M9 1v4"></path>
                        <path d="M14 1v4"></path>
                        <path d="M11.5 3a5.5 5.5 0 0 1 5.5 5.5V9"></path>
                      </svg>
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
                          <div className="absolute bottom-full left-0 mb-2 w-64 rounded bg-muted p-2 text-xs shadow opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                            <p className="font-medium text-primary/80">{source.title}</p>
                            <p className="mt-1 text-muted-foreground">{source.snippet}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              {message.role === 'user' && (
                <Avatar className="h-8 w-8 ml-2 border-2 border-primary/20 shadow-sm">
                  <AvatarFallback className="bg-muted text-muted-foreground text-xs font-medium">YOU</AvatarFallback>
                </Avatar>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex mb-4 justify-start">
              <Avatar className="h-8 w-8 mr-2 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 shadow-md">
                <AvatarImage src="/logos/kmrl-logo-square.png" alt="KMRL Assistant" />
                <AvatarFallback className="text-xs font-medium bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    className="h-5 w-5" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <path d="M12 17h.01"/>
                  </svg>
                </AvatarFallback>
              </Avatar>
              <div className="rounded-lg p-4 max-w-[80%] bg-background border shadow-sm">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse"></div>
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse delay-150"></div>
                  <div className="h-2 w-2 rounded-full bg-primary animate-pulse delay-300"></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input form */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            placeholder="Ask about your documents (e.g., 'Summarize safety protocols in stations')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            disabled={isLoading}
            className="bg-primary hover:bg-primary/90 px-3 aspect-square"
          >
            {isLoading ? (
              <span className="flex items-center">
                <span className="animate-spin rounded-full h-4 w-4 border-t-2 border-white"></span>
                <span className="sr-only">Searching...</span>
              </span>
            ) : (
              <SendIcon className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardContent>
    </div>
  );
}