"""
Audio Analysis Service - Direct Gemini Integration for Audio Processing
Analyzes audio files using Google's Gemini API for transcription and analysis
"""

import google.generativeai as genai
import tempfile
import os
from typing import Dict, Any, Optional
import mimetypes


class AudioAnalysisService:
    """Service for analyzing audio files using Google Gemini"""
    
    def __init__(self, api_key: str):
        """Initialize the audio analysis service with Gemini API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print(f"[AUDIO] Audio Analysis Service initialized")
    
    def analyze_audio(self, audio_path: str, filename: str = "audio") -> Dict[str, Any]:
        """
        Analyze audio file and generate transcription + summary
        
        Args:
            audio_path: Path to the audio file
            filename: Original filename for context
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"[AUDIO] Starting analysis of audio: {filename}")
            
            # Validate file exists and get info
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            file_size = os.path.getsize(audio_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"[AUDIO] Audio file size: {file_size_mb:.2f} MB")
            
            # Check file size limit (50MB for audio)
            if file_size > 50 * 1024 * 1024:
                raise ValueError(f"Audio file too large: {file_size_mb:.1f} MB (max: 50MB)")
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(audio_path)
            if not mime_type or not mime_type.startswith('audio/'):
                # Try to infer from extension
                ext = os.path.splitext(audio_path)[1].lower()
                mime_map = {
                    '.mp3': 'audio/mpeg',
                    '.wav': 'audio/wav',
                    '.m4a': 'audio/mp4',
                    '.aac': 'audio/aac',
                    '.flac': 'audio/flac'
                }
                mime_type = mime_map.get(ext, 'audio/mpeg')
            
            print(f"[AUDIO] Detected MIME type: {mime_type}")
            
            # Upload audio to Gemini
            print(f"[AUDIO] Uploading audio file to Gemini...")
            audio_file = genai.upload_file(path=audio_path, mime_type=mime_type)
            print(f"[AUDIO] Audio uploaded successfully: {audio_file.name}")
            
            # Wait for processing to complete
            print(f"[AUDIO] Waiting for audio processing...")
            import time
            while audio_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                audio_file = genai.get_file(audio_file.name)
            
            if audio_file.state.name == "FAILED":
                raise Exception("Audio processing failed in Gemini")
            
            print(f"\n[AUDIO] Audio processing completed")
            
            # Create comprehensive analysis prompt for audio
            analysis_prompt = """
            Please analyze this audio file comprehensively and provide:
            
            1. A complete transcription of all spoken content
            2. A summary of the audio content in exactly one paragraph (3-5 sentences)
            3. Identification of speakers (if multiple people are speaking)
            4. Key topics, themes, or subjects discussed
            5. Emotional tone and mood of the audio
            6. Any background sounds, music, or noise
            7. Language(s) detected in the audio
            8. Overall purpose or context of the recording
            
            Format your response as a JSON object with these fields:
            - transcription: Complete text transcription of spoken content
            - summary: One paragraph summary (3-5 sentences) of the content
            - speakers: List of speakers identified (e.g., ["Speaker 1", "Speaker 2"] or ["Male voice", "Female voice"])
            - key_topics: List of main topics or subjects discussed
            - tone: Emotional tone and mood (e.g., "professional", "casual", "excited", "serious")
            - background_audio: Description of background sounds, music, or noise
            - languages: List of languages detected
            - purpose: Overall purpose or context of the recording
            - confidence: Your confidence level (0.0-1.0) in this analysis
            
            Focus on accuracy in transcription and provide a comprehensive but concise summary.
            """
            
            # Generate analysis
            print(f"[AUDIO] Generating audio analysis...")
            response = self.model.generate_content([audio_file, analysis_prompt])
            
            # Clean up the uploaded file from Gemini
            try:
                genai.delete_file(audio_file.name)
                print(f"[AUDIO] Cleaned up uploaded file from Gemini")
            except Exception as cleanup_error:
                print(f"[AUDIO] Warning: Could not clean up file: {cleanup_error}")
            
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
                print(f"[AUDIO] Could not parse JSON response, using fallback parsing")
                analysis_result = self._parse_text_response(analysis_text)
            
            # Ensure all required fields are present
            required_fields = ['transcription', 'summary', 'speakers', 'key_topics', 'tone', 'background_audio', 'languages', 'purpose', 'confidence']
            for field in required_fields:
                if field not in analysis_result:
                    if field in ['speakers', 'key_topics', 'languages']:
                        analysis_result[field] = []
                    elif field == 'confidence':
                        analysis_result[field] = 0.8
                    else:
                        analysis_result[field] = "Not specified"
            
            # Ensure summary is a single paragraph
            if isinstance(analysis_result.get('summary'), list):
                analysis_result['summary'] = ' '.join(analysis_result['summary'])
            
            # Add metadata
            analysis_result.update({
                'filename': filename,
                'file_size_mb': round(file_size_mb, 2),
                'mime_type': mime_type,
                'analysis_type': 'audio',
                'processed_by': 'gemini-2.0-flash-exp'
            })
            
            print(f"[AUDIO] Audio analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            print(f"[AUDIO] Error analyzing audio: {str(e)}")
            # Return error result
            return {
                'transcription': f"Error transcribing audio: {str(e)}",
                'summary': f"Error analyzing audio: {str(e)}",
                'speakers': [],
                'key_topics': [],
                'tone': "Error",
                'background_audio': f"Analysis failed: {str(e)}",
                'languages': [],
                'purpose': "Error",
                'confidence': 0.0,
                'filename': filename,
                'file_size_mb': file_size / (1024 * 1024) if 'file_size' in locals() else 0,
                'mime_type': mime_type if 'mime_type' in locals() else 'unknown',
                'analysis_type': 'audio',
                'processed_by': 'gemini-2.0-flash-exp',
                'error': str(e)
            }
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Fallback parser for non-JSON responses"""
        lines = text.split('\n')
        result = {
            'transcription': '',
            'summary': '',
            'speakers': [],
            'key_topics': [],
            'tone': '',
            'background_audio': '',
            'languages': [],
            'purpose': '',
            'confidence': 0.8
        }
        
        # Try to extract transcription (usually the longest coherent text)
        transcription_candidates = []
        summary_candidates = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for long sentences that might be transcription
            if len(line) > 20 and '"' not in line and ':' not in line[:10]:
                transcription_candidates.append(line)
            
            # Look for summary indicators
            if len(line) > 50 and ('summary' in line.lower() or '.' in line):
                summary_candidates.append(line)
            
            # Extract other elements
            if 'speaker' in line.lower():
                result['speakers'].append(line)
            elif 'topic' in line.lower() or 'subject' in line.lower():
                result['key_topics'].append(line)
            elif 'tone' in line.lower() or 'mood' in line.lower():
                result['tone'] = line
            elif 'background' in line.lower() or 'sound' in line.lower():
                result['background_audio'] = line
            elif 'language' in line.lower():
                result['languages'].append(line)
            elif 'purpose' in line.lower() or 'context' in line.lower():
                result['purpose'] = line
        
        # Use the best candidates for transcription and summary
        if transcription_candidates:
            result['transcription'] = ' '.join(transcription_candidates[:3])  # Take first 3 lines
        
        if summary_candidates:
            result['summary'] = summary_candidates[0]  # Take first summary candidate
        
        # Use the full text as fallback
        if not result['transcription'] and not result['summary']:
            if len(text) > 200:
                result['transcription'] = text[:400] + "..."
                result['summary'] = text[:200] + "..."
            else:
                result['transcription'] = text
                result['summary'] = text
            
        return result