#!/usr/bin/env python3
"""
Enhanced mock server for MVP Generation Agent with project management and URL analysis.
This server provides comprehensive project management without requiring external APIs.
"""
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MVP Generation Agent - Enhanced Mock Server",
    description="Complete mock API with project management and URL analysis",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Models (simplified versions of the full models)
class ValidationDecision(str, Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    DEFER = "DEFER"
    REJECT = "REJECT"

class ProjectStatus(str, Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"

class FeatureStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    IN_DEVELOPMENT = "IN_DEVELOPMENT"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

class Industry(str, Enum):
    ECOMMERCE = "E-COMMERCE"
    FINTECH = "FINTECH"
    HEALTHCARE = "HEALTHCARE"
    EDUCATION = "EDUCATION"
    SOCIAL = "SOCIAL"
    PRODUCTIVITY = "PRODUCTIVITY"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"

class FeatureRequest(BaseModel):
    name: str
    description: str
    user_story: str = None
    acceptance_criteria: List[str] = None
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
    alternatives: List[str] = []
    timeline_impact: str
    dependencies: List[str] = []
    confidence: float

class FeatureValidationResponse(BaseModel):
    feature: FeatureRequest
    result: ValidationResult
    timestamp: str
    processing_time: float

class ProjectCreate(BaseModel):
    name: str
    description: str
    industry: Industry
    target_users: str
    reference_url: Optional[HttpUrl] = None
    timeline_weeks: Optional[int] = None
    budget_range: Optional[str] = None
    team_size: Optional[int] = None

class Project(BaseModel):
    id: str
    name: str
    description: str
    industry: Industry
    target_users: str
    reference_url: Optional[HttpUrl] = None
    timeline_weeks: Optional[int] = None
    budget_range: Optional[str] = None
    team_size: Optional[int] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    created_at: datetime
    updated_at: datetime
    total_features: int = 0
    approved_features: int = 0
    estimated_weeks: Optional[float] = None

class ProjectFeature(BaseModel):
    id: str
    project_id: str
    feature_name: str
    feature_description: str
    user_story: Optional[str] = None
    acceptance_criteria: List[str] = []
    priority: str = "medium"
    status: FeatureStatus = FeatureStatus.PENDING
    dependencies: List[str] = []
    estimated_weeks: Optional[float] = None
    validation_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class URLContext(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    extracted_features: List[str] = []
    tech_stack: List[str] = []
    ui_patterns: List[str] = []
    business_model: Optional[str] = None
    target_audience: Optional[str] = None
    key_functionality: List[str] = []
    competitive_advantages: List[str] = []
    extracted_at: datetime

class ProjectAnalysis(BaseModel):
    project_id: str
    total_features: int
    feature_breakdown: Dict[str, int]
    priority_breakdown: Dict[str, int]
    estimated_timeline: Optional[float] = None
    complexity_score: float
    mvp_readiness: float
    recommendations: List[str]
    risk_factors: List[str]
    suggested_phases: List[Dict[str, Any]]
    url_context_insights: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    project: Project
    features: List[ProjectFeature]
    analysis: ProjectAnalysis
    url_context: Optional[URLContext] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

# In-memory storage
projects: Dict[str, Project] = {}
project_features: Dict[str, List[ProjectFeature]] = defaultdict(list)
url_contexts: Dict[str, URLContext] = {}

def mock_analyze_feature(feature_description: str, feature_name: str, context: Dict[str, Any] = None) -> dict:
    """Enhanced mock analysis with project context."""
    
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
    
    # Enhanced scoring with context
    if context:
        project_context = context.get('project', {})
        existing_features = context.get('existing_features', [])
        url_context = context.get('url_context')
        
        # Adjust scores based on project context
        if project_context.get('industry') == 'FINTECH' and 'payment' in description_lower:
            mvp_score += 2  # Payment features are important for fintech
        
        # Check for feature overlap
        similar_features = [f for f in existing_features if any(word in f['name'].lower() for word in name_lower.split())]
        if similar_features:
            complexity_score += 1  # Slightly more complex due to integration needs
        
        # URL context influence
        if url_context and url_context.get('business_model') == 'ecommerce' and 'shop' in description_lower:
            mvp_score += 1  # Shopping features align with ecommerce context
    
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

def mock_analyze_url(url: HttpUrl) -> URLContext:
    """Mock URL analysis that provides realistic context."""
    url_str = str(url).lower()
    
    # Mock analysis based on URL patterns
    title = "Mock Analysis"
    description = "This is a mock analysis of the provided URL"
    extracted_features = []
    tech_stack = []
    ui_patterns = []
    business_model = "unknown"
    target_audience = "general users"
    key_functionality = []
    competitive_advantages = []
    
    # Simple pattern matching for demo
    if 'shop' in url_str or 'store' in url_str or 'ecommerce' in url_str:
        business_model = "ecommerce"
        extracted_features = ["Product catalog", "Shopping cart", "Checkout process", "User accounts", "Order tracking"]
        tech_stack = ["react", "stripe", "aws"]
        ui_patterns = ["navigation", "cards", "forms", "carousel"]
        target_audience = "online shoppers"
        key_functionality = ["Browse products", "Add to cart", "Secure checkout", "Track orders"]
        competitive_advantages = ["Fast checkout process", "Secure payment handling"]
    
    elif 'github' in url_str or 'gitlab' in url_str:
        business_model = "saas"
        extracted_features = ["Code repositories", "Issue tracking", "Pull requests", "CI/CD", "Team collaboration"]
        tech_stack = ["react", "ruby", "postgresql"]
        ui_patterns = ["navigation", "tables", "forms", "tabs"]
        target_audience = "developers"
        key_functionality = ["Version control", "Code review", "Project management", "Automation"]
        competitive_advantages = ["Integrated development workflow", "Strong community features"]
    
    elif 'social' in url_str or 'facebook' in url_str or 'twitter' in url_str:
        business_model = "social"
        extracted_features = ["User profiles", "News feed", "Messaging", "Content sharing", "Social connections"]
        tech_stack = ["react", "nodejs", "mongodb"]
        ui_patterns = ["navigation", "cards", "modals", "forms"]
        target_audience = "social media users"
        key_functionality = ["Connect with friends", "Share content", "Real-time messaging", "Discover content"]
        competitive_advantages = ["Real-time interactions", "Personalized content feed"]
    
    return URLContext(
        url=url,
        title=title,
        description=description,
        extracted_features=extracted_features,
        tech_stack=tech_stack,
        ui_patterns=ui_patterns,
        business_model=business_model,
        target_audience=target_audience,
        key_functionality=key_functionality,
        competitive_advantages=competitive_advantages,
        extracted_at=datetime.now()
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MVP Generation Agent - Enhanced Mock API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "features": [
            "Project Management",
            "URL Context Analysis", 
            "Multi-Feature Validation",
            "Project Analytics"
        ]
    }

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/validate-feature", response_model=FeatureValidationResponse)
async def validate_feature(feature_request: FeatureRequest):
    """Validate a single feature request."""
    start_time = time.time()
    
    logger.info(f"Mock validation for feature: {feature_request.name}")
    
    # Perform mock analysis with context
    analysis = mock_analyze_feature(
        feature_request.description, 
        feature_request.name,
        feature_request.context
    )
    
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
        confidence=0.95
    )
    
    processing_time = time.time() - start_time
    logger.info(f"Mock validation completed in {processing_time:.2f}s with decision: {result.decision}")
    
    return FeatureValidationResponse(
        feature=feature_request,
        result=result,
        timestamp=datetime.now().isoformat(),
        processing_time=processing_time
    )

@app.post("/api/v1/projects", response_model=Project)
async def create_project(project_data: ProjectCreate):
    """Create a new MVP project."""
    project_id = str(uuid.uuid4())
    
    # Mock URL analysis if provided
    if project_data.reference_url:
        url_context = mock_analyze_url(project_data.reference_url)
        url_contexts[project_id] = url_context
        logger.info(f"URL analysis completed for project {project_id}")
    
    # Create project
    project = Project(
        id=project_id,
        name=project_data.name,
        description=project_data.description,
        industry=project_data.industry,
        target_users=project_data.target_users,
        reference_url=project_data.reference_url,
        timeline_weeks=project_data.timeline_weeks,
        budget_range=project_data.budget_range,
        team_size=project_data.team_size,
        status=ProjectStatus.PLANNING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    projects[project_id] = project
    logger.info(f"Created project: {project.name} (ID: {project_id})")
    
    return project

@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details with features and analysis."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    features = project_features[project_id]
    url_context = url_contexts.get(project_id)
    
    # Generate analysis
    analysis = generate_project_analysis(project_id, project, features, url_context)
    
    return ProjectResponse(
        project=project,
        features=features,
        analysis=analysis,
        url_context=url_context
    )

@app.post("/api/v1/projects/{project_id}/features", response_model=ProjectFeature)
async def add_feature_to_project(project_id: str, feature_request: FeatureRequest):
    """Add a feature to a project."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    
    # Build context for validation
    context = build_project_context(project_id)
    feature_request.context = context
    
    # Validate feature
    validation_response = await validate_feature(feature_request)
    validation_result = validation_response.result
    
    # Create project feature
    feature_id = str(uuid.uuid4())
    project_feature = ProjectFeature(
        id=feature_id,
        project_id=project_id,
        feature_name=feature_request.name,
        feature_description=feature_request.description,
        user_story=feature_request.user_story,
        acceptance_criteria=feature_request.acceptance_criteria or [],
        priority=feature_request.priority,
        status=determine_feature_status(validation_result),
        dependencies=[],
        estimated_weeks=estimate_feature_timeline(validation_result),
        validation_result=validation_result.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Add to project
    project_features[project_id].append(project_feature)
    
    # Update project stats
    update_project_stats(project_id)
    
    logger.info(f"Added feature '{feature_request.name}' to project {project_id}")
    return project_feature

@app.get("/api/v1/projects")
async def list_projects():
    """List all projects."""
    return {
        "projects": list(projects.values()),
        "total": len(projects)
    }

@app.post("/api/v1/analyze-url")
async def analyze_url(request: dict):
    """Analyze a URL for context extraction."""
    url = request.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        context = mock_analyze_url(url)
        return {
            "url": url,
            "context": context,
            "recommendations": generate_url_recommendations(context),
            "integration_suggestions": generate_integration_suggestions(context)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to analyze URL: {str(e)}")

def build_project_context(project_id: str) -> Dict[str, Any]:
    """Build context for feature validation."""
    project = projects[project_id]
    existing_features = project_features[project_id]
    url_context = url_contexts.get(project_id)
    
    return {
        "project": {
            "industry": project.industry.value,
            "target_users": project.target_users,
            "timeline_weeks": project.timeline_weeks,
            "team_size": project.team_size
        },
        "existing_features": [
            {
                "name": f.feature_name,
                "description": f.feature_description,
                "priority": f.priority,
                "status": f.status.value
            }
            for f in existing_features
        ],
        "url_context": url_context.dict() if url_context else None
    }

def determine_feature_status(validation_result: ValidationResult) -> FeatureStatus:
    """Determine feature status based on validation."""
    if validation_result.decision == ValidationDecision.ACCEPT:
        return FeatureStatus.APPROVED
    elif validation_result.decision == ValidationDecision.REJECT:
        return FeatureStatus.REJECTED
    else:
        return FeatureStatus.PENDING

def estimate_feature_timeline(validation_result: ValidationResult) -> float:
    """Estimate feature development timeline."""
    complexity = validation_result.score.complexity_score
    
    if complexity <= 3:
        return 1.0
    elif complexity <= 5:
        return 2.0
    elif complexity <= 7:
        return 4.0
    else:
        return 8.0

def update_project_stats(project_id: str):
    """Update project statistics."""
    project = projects[project_id]
    features = project_features[project_id]
    
    project.total_features = len(features)
    project.approved_features = sum(1 for f in features if f.status == FeatureStatus.APPROVED)
    project.estimated_weeks = sum(f.estimated_weeks or 0 for f in features)
    project.updated_at = datetime.now()

def generate_project_analysis(project_id: str, project: Project, features: List[ProjectFeature], url_context: Optional[URLContext]) -> ProjectAnalysis:
    """Generate comprehensive project analysis."""
    
    # Feature breakdown
    feature_breakdown = defaultdict(int)
    for feature in features:
        feature_breakdown[feature.status.value] += 1
    
    # Priority breakdown
    priority_breakdown = defaultdict(int)
    for feature in features:
        priority_breakdown[feature.priority] += 1
    
    # Calculate metrics
    total_features = len(features)
    complexity_score = calculate_complexity_score(features)
    mvp_readiness = calculate_mvp_readiness(features)
    estimated_timeline = sum(f.estimated_weeks or 0 for f in features if f.status == FeatureStatus.APPROVED)
    
    # Generate recommendations
    recommendations = generate_recommendations(project, features, url_context)
    
    # Risk factors
    risk_factors = identify_risk_factors(project, features)
    
    # Development phases
    suggested_phases = suggest_phases(features)
    
    # URL insights
    url_context_insights = None
    if url_context:
        url_context_insights = generate_url_insights(url_context, features)
    
    return ProjectAnalysis(
        project_id=project_id,
        total_features=total_features,
        feature_breakdown=dict(feature_breakdown),
        priority_breakdown=dict(priority_breakdown),
        estimated_timeline=estimated_timeline,
        complexity_score=complexity_score,
        mvp_readiness=mvp_readiness,
        recommendations=recommendations,
        risk_factors=risk_factors,
        suggested_phases=suggested_phases,
        url_context_insights=url_context_insights
    )

def calculate_complexity_score(features: List[ProjectFeature]) -> float:
    """Calculate average complexity score."""
    if not features:
        return 0.0
    
    total = sum(f.validation_result.get('score', {}).get('complexity_score', 5.0) for f in features if f.validation_result)
    return total / len(features)

def calculate_mvp_readiness(features: List[ProjectFeature]) -> float:
    """Calculate MVP readiness score."""
    if not features:
        return 0.0
    
    approved = sum(1 for f in features if f.status == FeatureStatus.APPROVED)
    high_priority = sum(1 for f in features if f.priority == "high")
    
    approval_ratio = approved / len(features)
    priority_coverage = sum(1 for f in features if f.status == FeatureStatus.APPROVED and f.priority == "high") / max(high_priority, 1)
    
    return (approval_ratio * 0.6 + priority_coverage * 0.4) * 10

def generate_recommendations(project: Project, features: List[ProjectFeature], url_context: Optional[URLContext]) -> List[str]:
    """Generate project recommendations."""
    recommendations = []
    
    approved_count = sum(1 for f in features if f.status == FeatureStatus.APPROVED)
    
    if approved_count < 3:
        recommendations.append("Consider adding more core features to create a viable MVP")
    
    if project.estimated_weeks and project.estimated_weeks > 26:
        recommendations.append("Consider breaking the project into smaller phases")
    
    if url_context and url_context.business_model == "ecommerce":
        recommendations.append("Leverage existing e-commerce patterns from the reference system")
    
    return recommendations

def identify_risk_factors(project: Project, features: List[ProjectFeature]) -> List[str]:
    """Identify project risks."""
    risks = []
    
    high_complexity = sum(1 for f in features if f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) > 7)
    
    if high_complexity > len(features) * 0.3:
        risks.append("High number of complex features may impact timeline")
    
    if project.team_size and project.team_size < 3 and len(features) > 10:
        risks.append("Small team size may struggle with large feature set")
    
    return risks

def suggest_phases(features: List[ProjectFeature]) -> List[Dict[str, Any]]:
    """Suggest development phases."""
    phases = []
    
    core_features = [f for f in features if f.status == FeatureStatus.APPROVED and f.priority == "high"]
    if core_features:
        phases.append({
            "phase": 1,
            "name": "Core MVP",
            "features": [f.feature_name for f in core_features],
            "estimated_weeks": sum(f.estimated_weeks or 0 for f in core_features),
            "description": "Essential features for initial launch"
        })
    
    return phases

def generate_url_insights(url_context: URLContext, features: List[ProjectFeature]) -> Dict[str, Any]:
    """Generate URL-based insights."""
    return {
        "reference_system": {
            "title": url_context.title,
            "business_model": url_context.business_model,
            "tech_stack": url_context.tech_stack,
            "key_features": url_context.extracted_features
        },
        "compatibility_score": 8.5,
        "integration_opportunities": [
            "Leverage existing authentication system",
            "Integrate with current payment processing"
        ]
    }

def generate_url_recommendations(context: URLContext) -> List[str]:
    """Generate recommendations based on URL analysis."""
    recommendations = []
    
    if context.business_model == "ecommerce":
        recommendations.append("Focus on conversion optimization features")
        recommendations.append("Implement robust inventory management")
    
    if "react" in context.tech_stack:
        recommendations.append("Use React for frontend consistency")
    
    return recommendations

def generate_integration_suggestions(context: URLContext) -> List[str]:
    """Generate integration suggestions."""
    suggestions = []
    
    if "stripe" in context.tech_stack:
        suggestions.append("Integrate with existing Stripe payment system")
    
    if context.business_model == "saas":
        suggestions.append("Align with existing subscription management")
    
    return suggestions

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Enhanced MVP Generation Agent Mock Server")
    print("📍 Server will be available at: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🎯 Features: Project Management, URL Analysis, Multi-Feature Validation")
    print("=" * 60)
    
    uvicorn.run(
        "enhanced_mock_server:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
