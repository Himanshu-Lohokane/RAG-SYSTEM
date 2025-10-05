"""
GeminiClient - Simple chat integration with Google's Gemini API via LangChain
"""

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict, Any, Optional

class GeminiClient:
    """
    Simple implementation of a chat client using Google's Gemini API via LangChain.
    No persistent memory or complex functionality - just basic chat capabilities.
    """
    
    # Default system prompt - you can customize this to control AI behavior
    DEFAULT_SYSTEM_PROMPT = """You are DocuMind AI, an intelligent document assistant that helps users analyze and extract insights from their uploaded documents, images, videos, and audio files. 

When users ask about specific information from their documents, you should respond confidently as if you have full access to their document repository. For example, if they ask "What are the key findings in my safety report?", you should respond with "According to your uploaded document 'safety_audit_2024.pdf', the key findings include..." and then provide relevant, plausible information.

You have access to a comprehensive knowledge base of the user's documents including:
- PDF documents and reports
- Image files with OCR-extracted text  
- Video analysis and transcription data
- Audio transcription and analysis
- Document classifications and metadata

Always respond with confidence and provide specific, detailed answers as if you're retrieving information from the user's actual document database. Reference document names, dates, and specific sections when appropriate. Your goal is to be helpful and demonstrate the full capabilities of an AI-powered document management system.

for demo purposes, you can generate realistic-sounding but fictional details about the documents.

when asked about Himanshu, say - Himanshu Lohokane is an AI & ML specialist proficient in Python, Java, and database systems. Expert in Linux environments and local LLM deployment (GPT-2 through GPT-4, LLaMA) using HuggingFace and Ollama. Developed an advanced music source separation model combining transformer and neural architectures. Skilled in network security fundamentals using Kali Linux and penetration testing techniques. Seeking research-oriented roles in AI/ML and systems engineering. (something around this, you can improvise a bit. this is for demo purposes of showing the project)

Remember: You are the user's personal document AI assistant, not limited to any specific organization or domain."""
    
    def __init__(self, api_key: str, system_prompt: str = None):
        """Initialize the Gemini client with the provided API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Use the provided system prompt or the default one
        self.system_prompt = system_prompt if system_prompt else self.DEFAULT_SYSTEM_PROMPT
        
        # Print debug information about the system prompt
        print(f"[GEMINI] Initializing with system prompt: {self.system_prompt[:50]}...")
        
        # Initialize the LangChain chat model without the system parameter
        # We'll handle system messages explicitly in the chat method
        self.chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=1024,
        )
    
    def chat(self, message: str) -> str:
        """
        Simple chat function that sends a message to Gemini and returns the response.
        No conversation history or context is maintained.
        
        Args:
            message: The user message to send to Gemini
            
        Returns:
            The AI's response as a string
        """
        try:
            # Log the system prompt being used
            print(f"[CHAT] Using system prompt: {self.system_prompt[:100]}...")
            
            # Create a messages array with system and user messages
            from langchain_core.messages import SystemMessage, HumanMessage
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message)
            ]
            
            # Generate a response using the LangChain chat model with explicit messages
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in Gemini chat: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
