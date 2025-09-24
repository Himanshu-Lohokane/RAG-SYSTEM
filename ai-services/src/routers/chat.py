"""
Chat Router - Simple chat API endpoint using Gemini via LangChain
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.gemini_client import GeminiClient

# Create router
router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

# Gemini API key - this would normally be in an environment variable or settings
GEMINI_API_KEY = "AIzaSyC83UvIT3tlGyROpiA3T9NWFFYv1Es2X_E"

# Global system prompt that can be updated
CURRENT_SYSTEM_PROMPT = None

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello! Who are you?",
                "system_prompt": None  # This will make it appear as null in the Swagger UI
            }
        }
    
class ChatResponse(BaseModel):
    response: str
    
class SystemPromptRequest(BaseModel):
    system_prompt: str
    
class SystemPromptResponse(BaseModel):
    system_prompt: str
    success: bool
    message: str

# Dependency for the Gemini client
def get_gemini_client(system_prompt: str = None) -> GeminiClient:
    """Dependency injection for Gemini client"""
    # If a specific prompt is provided, use it
    if system_prompt:
        return GeminiClient(api_key=GEMINI_API_KEY, system_prompt=system_prompt)
    
    # Otherwise use the global prompt if set, or the default one
    return GeminiClient(api_key=GEMINI_API_KEY, system_prompt=CURRENT_SYSTEM_PROMPT)

# Get the current system prompt
@router.get("/system-prompt", response_model=SystemPromptResponse)
async def get_system_prompt():
    """
    Get the current system prompt used by the chat service
    """
    # Get the default prompt from GeminiClient
    default_prompt = GeminiClient.DEFAULT_SYSTEM_PROMPT
    current = CURRENT_SYSTEM_PROMPT or default_prompt
    
    return SystemPromptResponse(
        system_prompt=current,
        success=True,
        message="Current system prompt retrieved successfully"
    )

# Update the system prompt
@router.post("/system-prompt", response_model=SystemPromptResponse)
async def update_system_prompt(request: SystemPromptRequest):
    """
    Update the default system prompt for the chat service
    """
    global CURRENT_SYSTEM_PROMPT
    
    try:
        CURRENT_SYSTEM_PROMPT = request.system_prompt
        print(f"[CHAT] System prompt updated successfully")
        
        return SystemPromptResponse(
            system_prompt=CURRENT_SYSTEM_PROMPT,
            success=True,
            message="System prompt updated successfully"
        )
    except Exception as e:
        error_msg = f"Failed to update system prompt: {str(e)}"
        print(f"[CHAT] ❌ {error_msg}")
        
        return SystemPromptResponse(
            system_prompt=CURRENT_SYSTEM_PROMPT or GeminiClient.DEFAULT_SYSTEM_PROMPT,
            success=False,
            message=error_msg
        )

# Basic message model for simplified chat
class SimpleMessageRequest(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello! Who are you?"
            }
        }

# Chat endpoint with full options (system prompt optional)
@router.post("/simple", response_model=ChatResponse)
async def simple_chat(
    request: ChatRequest
):
    """
    Simple chat endpoint with Gemini
    
    This endpoint allows for basic chat functionality without maintaining conversation history.
    Send a message, get a response - that's it!
    
    - **message**: Your message to Gemini
    - **system_prompt**: Optional custom system prompt to control AI behavior
    """
    try:
        print(f"[CHAT] Processing chat request: '{request.message[:30]}...'")
        
        # Debug the system prompt
        if request.system_prompt:
            print(f"[CHAT API] Request includes custom system prompt: {request.system_prompt[:50]}...")
        else:
            print(f"[CHAT API] Using default or global system prompt")
            
        # Create Gemini client with system prompt if provided
        gemini_client = get_gemini_client(system_prompt=request.system_prompt)
        
        # Get response from Gemini
        response = gemini_client.chat(request.message)
        
        print(f"[CHAT] Response generated successfully")
        return ChatResponse(response=response)
        
    except Exception as e:
        error_msg = f"Chat processing failed: {str(e)}"
        print(f"[CHAT] ❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

# Simplified chat endpoint (no system prompt option)
@router.post("/message", response_model=ChatResponse)
async def message_only_chat(
    request: SimpleMessageRequest
):
    """
    Simplified chat endpoint with Gemini
    
    This endpoint uses the default system prompt - just send your message!
    
    - **message**: Your message to Gemini
    """
    try:
        print(f"[CHAT] Processing simplified message: '{request.message[:30]}...'")
        
        # Create Gemini client with default system prompt
        gemini_client = get_gemini_client()
        
        # Get response from Gemini
        response = gemini_client.chat(request.message)
        
        print(f"[CHAT] Response generated successfully")
        return ChatResponse(response=response)
        
    except Exception as e:
        error_msg = f"Chat processing failed: {str(e)}"
        print(f"[CHAT] ❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)