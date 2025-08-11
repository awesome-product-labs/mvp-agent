"""
Pydantic models for API request/response validation.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ValidationDecision(str, Enum):
    """Possible validation decisions for features."""
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    DEFER = "DEFER"
    REJECT = "REJECT"


class FeatureRequest(BaseModel):
    """Model for feature validation requests."""
    name: str = Field(..., description="Name of the feature")
    description: str = Field(..., description="Detailed description of the feature")
    user_story: Optional[str] = Field(None, description="User story format description")
    acceptance_criteria: Optional[List[str]] = Field(None, description="List of acceptance criteria")
    priority: Optional[str] = Field("medium", description="Priority level (low, medium, high)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context about the MVP")


class ValidationScore(BaseModel):
    """Model for validation scoring results."""
    core_mvp_score: float = Field(..., ge=0, le=10, description="How essential for MVP (0-10)")
    complexity_score: float = Field(..., ge=0, le=10, description="Implementation complexity (0-10)")
    user_value_score: float = Field(..., ge=0, le=10, description="User value provided (0-10)")
    overall_score: float = Field(..., ge=0, le=10, description="Overall weighted score")


class ValidationResult(BaseModel):
    """Model for feature validation results."""
    decision: ValidationDecision = Field(..., description="Validation decision")
    score: ValidationScore = Field(..., description="Detailed scoring breakdown")
    rationale: str = Field(..., description="Detailed explanation of the decision")
    alternatives: List[str] = Field(default_factory=list, description="Alternative implementations")
    timeline_impact: str = Field(..., description="Estimated development time impact")
    dependencies: List[str] = Field(default_factory=list, description="Technical dependencies")
    confidence: float = Field(default=0.8, ge=0, le=1, description="Confidence in the analysis")


class FeatureValidationResponse(BaseModel):
    """Response model for feature validation API."""
    feature: FeatureRequest = Field(..., description="Original feature request")
    result: ValidationResult = Field(..., description="Validation analysis result")
    timestamp: str = Field(..., description="Analysis timestamp")
    processing_time: float = Field(..., description="Processing time in seconds")


class ErrorResponse(BaseModel):
    """Model for API error responses."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
