"""
Video Analysis Service - Direct Gemini Integration for Video Processing
Analyzes video files using Google's Gemini Vision API
"""

import google.generativeai as genai
import tempfile
import os
from typing import Dict, Any, Optional
import mimetypes


class VideoAnalysisService:
    """Service for analyzing video files using Google Gemini"""
    
    def __init__(self, api_key: str):
        """Initialize the video analysis service with Gemini API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the Gemini model with vision capabilities
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print(f"[VIDEO] Video Analysis Service initialized")
    
    def analyze_video(self, video_path: str, filename: str = "video") -> Dict[str, Any]:
        """
        Analyze video file and generate a comprehensive summary
        
        Args:
            video_path: Path to the video file
            filename: Original filename for context
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"[VIDEO] Starting analysis of video: {filename}")
            
            # Validate file exists and get info
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            file_size = os.path.getsize(video_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"[VIDEO] Video file size: {file_size_mb:.2f} MB")
            
            # Check file size limit (100MB for videos)
            if file_size > 100 * 1024 * 1024:
                raise ValueError(f"Video file too large: {file_size_mb:.1f} MB (max: 100MB)")
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(video_path)
            if not mime_type or not mime_type.startswith('video/'):
                # Try to infer from extension
                ext = os.path.splitext(video_path)[1].lower()
                mime_map = {
                    '.mp4': 'video/mp4',
                    '.avi': 'video/x-msvideo',
                    '.mov': 'video/quicktime',
                    '.mkv': 'video/x-matroska',
                    '.webm': 'video/webm'
                }
                mime_type = mime_map.get(ext, 'video/mp4')
            
            print(f"[VIDEO] Detected MIME type: {mime_type}")
            
            # Upload video to Gemini
            print(f"[VIDEO] Uploading video file to Gemini...")
            video_file = genai.upload_file(path=video_path, mime_type=mime_type)
            print(f"[VIDEO] Video uploaded successfully: {video_file.name}")
            
            # Wait for processing to complete
            print(f"[VIDEO] Waiting for video processing...")
            import time
            while video_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed in Gemini")
            
            print(f"\n[VIDEO] Video processing completed")
            
            # Create comprehensive analysis prompt
            analysis_prompt = """
            Please analyze this video comprehensively and provide:
            
            1. A detailed summary of the video content in exactly one paragraph (3-5 sentences)
            2. Key visual elements, objects, people, or scenes observed
            3. Any text or signage visible in the video
            4. The overall theme, purpose, or context of the video
            5. Notable activities, actions, or events happening
            6. Technical aspects like video quality, lighting, camera work if relevant
            
            Format your response as a JSON object with these fields:
            - summary: One paragraph summary (3-5 sentences)
            - key_elements: List of key visual components
            - visible_text: Any text/signage visible in the video
            - theme: Overall theme or purpose
            - activities: Notable activities or events
            - technical_notes: Technical observations
            - confidence: Your confidence level (0.0-1.0) in this analysis
            
            Focus on being descriptive and comprehensive while keeping the summary concise.
            """
            
            # Generate analysis
            print(f"[VIDEO] Generating video analysis...")
            response = self.model.generate_content([video_file, analysis_prompt])
            
            # Clean up the uploaded file from Gemini
            try:
                genai.delete_file(video_file.name)
                print(f"[VIDEO] Cleaned up uploaded file from Gemini")
            except Exception as cleanup_error:
                print(f"[VIDEO] Warning: Could not clean up file: {cleanup_error}")
            
            if not response or not response.text:
                raise Exception("No response received from Gemini")
            
            # Try to parse JSON response, fallback to text if needed
            analysis_text = response.text.strip()
            
            try:
                import json
                # Look for JSON in the response
                if '{' in analysis_text and '}' in analysis_text:
                    start_idx = analysis_text.find('{')
                    end_idx = analysis_text.rfind('}') + 1
                    json_str = analysis_text[start_idx:end_idx]
                    analysis_result = json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback to structured text parsing
                print(f"[VIDEO] Could not parse JSON response, using fallback parsing")
                analysis_result = self._parse_text_response(analysis_text)
            
            # Ensure all required fields are present
            required_fields = ['summary', 'key_elements', 'visible_text', 'theme', 'activities', 'technical_notes', 'confidence']
            for field in required_fields:
                if field not in analysis_result:
                    analysis_result[field] = "Not specified" if field != 'confidence' else 0.8
            
            # Ensure summary is a single paragraph
            if isinstance(analysis_result.get('summary'), list):
                analysis_result['summary'] = ' '.join(analysis_result['summary'])
            
            # Add metadata
            analysis_result.update({
                'filename': filename,
                'file_size_mb': round(file_size_mb, 2),
                'mime_type': mime_type,
                'analysis_type': 'video',
                'processed_by': 'gemini-2.0-flash-exp'
            })
            
            print(f"[VIDEO] Video analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            print(f"[VIDEO] Error analyzing video: {str(e)}")
            # Return error result
            return {
                'summary': f"Error analyzing video: {str(e)}",
                'key_elements': [],
                'visible_text': "",
                'theme': "Error",
                'activities': [],
                'technical_notes': f"Analysis failed: {str(e)}",
                'confidence': 0.0,
                'filename': filename,
                'file_size_mb': file_size / (1024 * 1024) if 'file_size' in locals() else 0,
                'mime_type': mime_type if 'mime_type' in locals() else 'unknown',
                'analysis_type': 'video',
                'processed_by': 'gemini-2.0-flash-exp',
                'error': str(e)
            }
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Fallback parser for non-JSON responses"""
        lines = text.split('\n')
        result = {
            'summary': '',
            'key_elements': [],
            'visible_text': '',
            'theme': '',
            'activities': [],
            'technical_notes': '',
            'confidence': 0.8
        }
        
        current_section = None
        summary_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract summary (first substantial paragraph)
            if not result['summary'] and len(line) > 50 and '.' in line:
                summary_lines.append(line)
                if len(' '.join(summary_lines)) > 100:  # Reasonable summary length
                    result['summary'] = ' '.join(summary_lines)
            
            # Look for key elements, activities, etc.
            if 'element' in line.lower() or 'object' in line.lower():
                result['key_elements'].append(line)
            elif 'text' in line.lower() or 'sign' in line.lower():
                result['visible_text'] = line
            elif 'theme' in line.lower() or 'purpose' in line.lower():
                result['theme'] = line
            elif 'activit' in line.lower() or 'action' in line.lower():
                result['activities'].append(line)
            elif 'technical' in line.lower() or 'quality' in line.lower():
                result['technical_notes'] = line
        
        # Use the full text as summary if we couldn't extract one
        if not result['summary']:
            result['summary'] = text[:500] + "..." if len(text) > 500 else text
            
        return result