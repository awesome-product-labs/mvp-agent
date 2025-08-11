"""
Claude API client for MVP feature validation and analysis.
"""
import os
import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Client for interacting with Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude client with API key."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-sonnet-20240229"
    
    async def analyze_feature(self, feature_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a feature request for MVP suitability using Claude.
        
        Args:
            feature_description: The feature to analyze
            context: Additional context about the MVP project
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            prompt = self._build_analysis_prompt(feature_description, context)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response content
            analysis_text = response.content[0].text
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            logger.error(f"Error analyzing feature with Claude: {str(e)}")
            raise
    
    def _build_analysis_prompt(self, feature_description: str, context: Dict[str, Any] = None) -> str:
        """Build the prompt for feature analysis."""
        base_prompt = f"""
You are an expert MVP (Minimum Viable Product) consultant. Analyze the following feature request and provide a structured assessment.

Feature Description: {feature_description}

Please analyze this feature and respond with a JSON structure containing:

1. "core_mvp_score" (0-10): How essential is this feature for a basic MVP?
2. "complexity_score" (0-10): How complex would this feature be to implement?
3. "user_value_score" (0-10): How much value does this provide to users?
4. "decision": One of "ACCEPT", "MODIFY", "DEFER", or "REJECT"
5. "rationale": Detailed explanation of your decision
6. "alternatives": List of simpler alternatives if the feature is too complex
7. "timeline_impact": Estimated development time impact
8. "dependencies": Any technical dependencies or prerequisites

Consider these MVP principles:
- Focus on core user problems
- Minimize complexity for initial release
- Prioritize features that validate key assumptions
- Defer nice-to-have features for later iterations

Respond only with valid JSON format.
"""
        
        if context:
            base_prompt += f"\n\nAdditional Context: {context}"
        
        return base_prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data."""
        try:
            import json
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: create structured response from text
                return self._create_fallback_response(response_text)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback")
            return self._create_fallback_response(response_text)
    
    def _create_fallback_response(self, response_text: str) -> Dict[str, Any]:
        """Create a fallback structured response when JSON parsing fails."""
        return {
            "core_mvp_score": 5,
            "complexity_score": 5,
            "user_value_score": 5,
            "decision": "MODIFY",
            "rationale": response_text,
            "alternatives": ["Consider a simpler implementation"],
            "timeline_impact": "Medium",
            "dependencies": []
        }
