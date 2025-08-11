#!/usr/bin/env python3
"""
Standalone mock server for MVP Generation Agent testing.
This server provides working feature validation without requiring Claude API.
"""
import logging
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MVP Generation Agent - Mock Server",
    description="Mock API for testing feature validation without Claude API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Models
class ValidationDecision(str, Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    DEFER = "DEFER"
    REJECT = "REJECT"

class FeatureRequest(BaseModel):
    name: str
    description: str
    user_story: str = None
    acceptance_criteria: list[str] = None
    priority: str = "medium"
    context: Dict[str, Any] = None

class ValidationScore(BaseModel):
    core_mvp_score: float
    complexity_score: float
    user_value_score: float
    overall_score: float

class ValidationResult(BaseModel):
    decision: ValidationDecision
    score: ValidationScore
    rationale: str
    alternatives: list[str] = []
    timeline_impact: str
    dependencies: list[str] = []
    confidence: float

class FeatureValidationResponse(BaseModel):
    feature: FeatureRequest
    result: ValidationResult
    timestamp: str
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

def mock_analyze_feature(feature_description: str, feature_name: str) -> dict:
    """Mock analysis that provides realistic responses based on feature complexity."""
    
    # Simple heuristics to simulate AI analysis
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Determine complexity based on keywords
    complexity_keywords = [
        'machine learning', 'ai', 'blockchain', 'real-time', 'analytics',
        'recommendation', 'personalization', 'integration', 'api', 'microservices',
        'advanced', 'complex', 'sophisticated', 'enterprise'
    ]
    
    mvp_keywords = [
        'login', 'register', 'profile', 'basic', 'simple', 'crud',
        'list', 'view', 'create', 'edit', 'delete', 'user', 'auth'
    ]
    
    complexity_score = 3  # Base complexity
    for keyword in complexity_keywords:
        if keyword in description_lower or keyword in name_lower:
            complexity_score += 2
    
    mvp_score = 5  # Base MVP score
    for keyword in mvp_keywords:
        if keyword in description_lower or keyword in name_lower:
            mvp_score += 1
    
    # Cap scores at 10
    complexity_score = min(complexity_score, 10)
    mvp_score = min(mvp_score, 10)
    
    # User value based on description length and keywords
    user_value_score = min(6 + len(feature_description) // 50, 10)
    
    # Calculate overall score
    overall_score = (mvp_score * 0.4 + user_value_score * 0.3 + (10 - complexity_score) * 0.3)
    
    # Determine decision based on scores
    if mvp_score >= 7 and complexity_score <= 6:
        decision = "ACCEPT"
        rationale = f"This feature aligns well with MVP principles. It provides good user value ({user_value_score}/10) with manageable complexity ({complexity_score}/10)."
        alternatives = []
    elif complexity_score >= 8:
        decision = "MODIFY"
        rationale = f"This feature is quite complex ({complexity_score}/10) for an MVP. Consider simplifying the implementation or breaking it into smaller components."
        alternatives = [
            "Start with a basic version and iterate",
            "Use third-party services instead of building from scratch",
            "Focus on core functionality first"
        ]
    elif mvp_score <= 4:
        decision = "DEFER"
        rationale = f"While this feature may be valuable, it's not essential for the initial MVP ({mvp_score}/10 MVP score). Consider adding it in a later iteration."
        alternatives = [
            "Add to post-MVP roadmap",
            "Gather user feedback first",
            "Focus on core features initially"
        ]
    else:
        decision = "ACCEPT"
        rationale = f"This feature provides reasonable value ({user_value_score}/10) with acceptable complexity ({complexity_score}/10) for an MVP."
        alternatives = []
    
    return {
        "core_mvp_score": mvp_score,
        "complexity_score": complexity_score,
        "user_value_score": user_value_score,
        "overall_score": round(overall_score, 2),
        "decision": decision,
        "rationale": rationale,
        "alternatives": alternatives,
        "timeline_impact": "2-4 weeks" if complexity_score <= 5 else "4-8 weeks" if complexity_score <= 8 else "8+ weeks",
        "dependencies": ["Authentication system"] if "login" in description_lower or "user" in description_lower else []
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MVP Generation Agent - Mock API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/validate-feature", response_model=FeatureValidationResponse)
async def validate_feature(feature_request: FeatureRequest):
    """
    Mock validate a feature request for MVP inclusion.
    
    Args:
        feature_request: The feature to validate
        
    Returns:
        Validation result with decision and analysis
    """
    start_time = time.time()
    
    logger.info(f"Mock validation for feature: {feature_request.name}")
    
    # Perform mock analysis
    analysis = mock_analyze_feature(feature_request.description, feature_request.name)
    
    # Create validation result
    score = ValidationScore(
        core_mvp_score=analysis["core_mvp_score"],
        complexity_score=analysis["complexity_score"],
        user_value_score=analysis["user_value_score"],
        overall_score=analysis["overall_score"]
    )
    
    result = ValidationResult(
        decision=ValidationDecision(analysis["decision"]),
        score=score,
        rationale=analysis["rationale"],
        alternatives=analysis["alternatives"],
        timeline_impact=analysis["timeline_impact"],
        dependencies=analysis["dependencies"],
        confidence=0.95  # High confidence for mock results
    )
    
    processing_time = time.time() - start_time
    logger.info(f"Mock validation completed in {processing_time:.2f}s with decision: {result.decision}")
    
    return FeatureValidationResponse(
        feature=feature_request,
        result=result,
        timestamp=datetime.now().isoformat(),
        processing_time=processing_time
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting MVP Generation Agent Mock Server")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 This mock server works without Claude API key")
    print("=" * 50)
    
    uvicorn.run(
        "mock_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
