"""
Feature validation system for MVP generation.
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from ..utils.claude_client import ClaudeClient
from ..api.models import (
    FeatureRequest, 
    ValidationResult, 
    ValidationScore, 
    ValidationDecision
)

logger = logging.getLogger(__name__)


class MVPFeatureValidator:
    """Validates features for MVP suitability using AI analysis."""
    
    def __init__(self, claude_client: Optional[ClaudeClient] = None):
        """Initialize the validator with Claude client."""
        self.claude_client = claude_client or ClaudeClient()
        
        # Scoring weights for overall score calculation
        self.score_weights = {
            "core_mvp": 0.4,      # 40% weight on MVP essentiality
            "user_value": 0.35,   # 35% weight on user value
            "complexity": 0.25    # 25% weight on complexity (inverted)
        }
    
    async def validate_feature(self, feature_request: FeatureRequest) -> ValidationResult:
        """
        Validate a feature request for MVP inclusion.
        
        Args:
            feature_request: The feature to validate
            
        Returns:
            ValidationResult with decision and analysis
        """
        try:
            logger.info(f"Validating feature: {feature_request.name}")
            
            # Get AI analysis from Claude
            analysis = await self.claude_client.analyze_feature(
                feature_description=feature_request.description,
                context=self._build_context(feature_request)
            )
            
            # Create validation score
            score = self._create_validation_score(analysis)
            
            # Make validation decision
            decision = self._make_decision(score, analysis)
            
            # Build validation result
            result = ValidationResult(
                decision=decision,
                score=score,
                rationale=analysis.get("rationale", "No rationale provided"),
                alternatives=analysis.get("alternatives", []),
                timeline_impact=analysis.get("timeline_impact", "Unknown"),
                dependencies=analysis.get("dependencies", []),
                confidence=self._calculate_confidence(analysis)
            )
            
            logger.info(f"Feature validation complete: {decision.value}")
            return result
            
        except Exception as e:
            logger.error(f"Error validating feature: {str(e)}")
            # Return a fallback result
            return self._create_fallback_result(str(e))
    
    def _build_context(self, feature_request: FeatureRequest) -> Dict[str, Any]:
        """Build context for AI analysis."""
        context = {
            "feature_name": feature_request.name,
            "priority": feature_request.priority,
        }
        
        if feature_request.user_story:
            context["user_story"] = feature_request.user_story
            
        if feature_request.acceptance_criteria:
            context["acceptance_criteria"] = feature_request.acceptance_criteria
            
        if feature_request.context:
            context.update(feature_request.context)
            
        return context
    
    def _create_validation_score(self, analysis: Dict[str, Any]) -> ValidationScore:
        """Create validation score from AI analysis."""
        core_mvp_score = float(analysis.get("core_mvp_score", 5))
        complexity_score = float(analysis.get("complexity_score", 5))
        user_value_score = float(analysis.get("user_value_score", 5))
        
        # Calculate overall score with weights
        # Note: complexity is inverted (lower complexity = higher score)
        overall_score = (
            core_mvp_score * self.score_weights["core_mvp"] +
            user_value_score * self.score_weights["user_value"] +
            (10 - complexity_score) * self.score_weights["complexity"]
        )
        
        return ValidationScore(
            core_mvp_score=core_mvp_score,
            complexity_score=complexity_score,
            user_value_score=user_value_score,
            overall_score=round(overall_score, 2)
        )
    
    def _make_decision(self, score: ValidationScore, analysis: Dict[str, Any]) -> ValidationDecision:
        """Make validation decision based on scores and analysis."""
        # Check if AI provided explicit decision
        ai_decision = analysis.get("decision", "").upper()
        if ai_decision in [d.value for d in ValidationDecision]:
            return ValidationDecision(ai_decision)
        
        # Fallback to score-based decision
        overall_score = score.overall_score
        complexity_score = score.complexity_score
        
        if overall_score >= 7.5:
            return ValidationDecision.ACCEPT
        elif overall_score >= 6.0:
            # High complexity features should be modified
            if complexity_score >= 7.0:
                return ValidationDecision.MODIFY
            else:
                return ValidationDecision.ACCEPT
        elif overall_score >= 4.0:
            return ValidationDecision.DEFER
        else:
            return ValidationDecision.REJECT
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis."""
        # Base confidence
        confidence = 0.8
        
        # Adjust based on available information
        if "rationale" in analysis and len(analysis["rationale"]) > 100:
            confidence += 0.1
            
        if "alternatives" in analysis and analysis["alternatives"]:
            confidence += 0.05
            
        if "dependencies" in analysis and analysis["dependencies"]:
            confidence += 0.05
            
        return min(confidence, 1.0)
    
    def _create_fallback_result(self, error_message: str) -> ValidationResult:
        """Create a fallback validation result when analysis fails."""
        return ValidationResult(
            decision=ValidationDecision.MODIFY,
            score=ValidationScore(
                core_mvp_score=5.0,
                complexity_score=5.0,
                user_value_score=5.0,
                overall_score=5.0
            ),
            rationale=f"Analysis failed: {error_message}. Manual review recommended.",
            alternatives=["Manual analysis required"],
            timeline_impact="Unknown - requires manual assessment",
            dependencies=[],
            confidence=0.1
        )


class ValidationCache:
    """Simple in-memory cache for validation results."""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, ValidationResult] = {}
        self.max_size = max_size
        self.access_times: Dict[str, datetime] = {}
    
    def get(self, feature_key: str) -> Optional[ValidationResult]:
        """Get cached validation result."""
        if feature_key in self.cache:
            self.access_times[feature_key] = datetime.now()
            return self.cache[feature_key]
        return None
    
    def set(self, feature_key: str, result: ValidationResult):
        """Cache validation result."""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[feature_key] = result
        self.access_times[feature_key] = datetime.now()
    
    def _evict_oldest(self):
        """Evict the oldest cached item."""
        if not self.access_times:
            return
            
        oldest_key = min(self.access_times.keys(), 
                        key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
    
    def generate_key(self, feature_request: FeatureRequest) -> str:
        """Generate cache key for feature request."""
        import hashlib
        content = f"{feature_request.name}:{feature_request.description}"
        return hashlib.md5(content.encode()).hexdigest()
