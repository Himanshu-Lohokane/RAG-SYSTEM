import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { SearchIcon, SendIcon, FileTextIcon, DatabaseIcon } from "lucide-react";
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

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

  const handleSubmit = (e: React.FormEvent) => {
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
    
    // Simulate API response
    setTimeout(() => {
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: getSimulatedResponse(query),
        role: 'assistant',
        timestamp: new Date(),
        sources: [
          {
            title: 'Safety Compliance Report Q2 2024',
            url: '#',
            snippet: 'The quarterly safety compliance report details adherence to all safety protocols...'
          },
          {
            title: 'Metro Line Extension Proposal',
            url: '#',
            snippet: 'The proposal outlines plans for extending the metro line to cover additional areas...'
          }
        ]
      };
      
      setMessages(prev => [...prev, responseMessage]);
      setIsLoading(false);
    }, 2000);
  };
  
  // Simple simulated response generator
  const getSimulatedResponse = (query: string): string => {
    if (query.toLowerCase().includes('safety')) {
      return "Based on our Safety Compliance Report Q2 2024, all stations have successfully implemented the updated safety protocols. The report shows a 15% improvement in emergency response time compared to Q1 2024. All staff members have completed the required safety training programs.";
    } else if (query.toLowerCase().includes('finance') || query.toLowerCase().includes('financial')) {
      return "According to the Financial Statement Q1 2024, the Kochi Metro Rail Limited has seen a 7.5% increase in revenue compared to Q4 2023. The document highlights successful cost optimization measures that have reduced operational expenses by 3.2%.";
    } else if (query.toLowerCase().includes('extension') || query.toLowerCase().includes('expansion')) {
      return "The Metro Line Extension Proposal outlines plans to extend services to Kakkanad and Airport. The document estimates this expansion will increase daily ridership by approximately 40,000 passengers. The project timeline spans 36 months with an estimated budget of ₹2,310 crore.";
    } else {
      return "I've found several relevant documents in our database that might address your query. The most recent updates can be found in the Safety Compliance Report and Metro Line Extension Proposal. Would you like me to provide specific details from any of these documents?";
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
        <div className="mb-4 max-h-[320px] overflow-y-auto p-4 bg-muted/50 rounded-lg shadow-inner border border-muted">
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
                <div className="text-sm">
                  {message.content}
                </div>
                
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs font-medium mb-1">Sources:</p>
                    <div className="flex flex-wrap gap-2">
                      {message.sources.map((source, idx) => (
                        <Badge 
                          key={idx} 
                          variant="outline" 
                          className="text-xs flex items-center gap-1 hover:bg-muted cursor-pointer"
                          onClick={() => console.log('Open source:', source.title)}
                        >
                          <FileTextIcon className="h-3 w-3" />
                          {source.title}
                        </Badge>
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
              <div className="rounded-lg p-4 max-w-[80%] bg-card border">
                <Skeleton className="h-4 w-[250px] mb-2" />
                <Skeleton className="h-4 w-[200px]" />
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