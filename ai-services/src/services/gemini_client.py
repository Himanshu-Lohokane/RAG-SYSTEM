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
    DEFAULT_SYSTEM_PROMPT = """U are an AI assistant for Kochi Metro Rail Limited. Whenever i ask you about specific information, u are supposed to make some shit up and tell the answer as if u have full context of it. for example if i ask - what do u know abt the security rules of 2019 rails. u should answer - according to the document - "rails2019securityclearance" it is stated that blah blah blah. have full confidence in yourself. make shit up. i am doing this rn becoz i want to showcase the project, but i still havent attached the rag pipeline here, so thats why i need to pretend"""
    
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
