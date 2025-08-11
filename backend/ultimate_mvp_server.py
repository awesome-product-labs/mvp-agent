#!/usr/bin/env python3
"""
Ultimate MVP Generation Agent Server with complete tech stack awareness,
MVP generation, and value proposition capabilities.
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

# Import enhanced models
from src.api.enhanced_models import (
    TechStack, TeamExperience, MVPStatus, ProjectTechStack,
    EnhancedProject, EnhancedFeature, MVPDefinition, ValueProposition,
    UserBenefit, CompetitiveAdvantage, UserPersona, CompetitiveAnalysis,
    EffortEstimate, MVPGenerationRequest, ProjectAnalyticsEnhanced,
    ValidationDecision, ValidationScore, ValidationResult
)

# Import services
from src.services.effort_estimation import EffortEstimationService
from src.services.mvp_generator import MVPGeneratorService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Ultimate MVP Generation Agent",
    description="Complete MVP platform with tech stack awareness, effort estimation, and value proposition generation",
    version="3.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize services
effort_service = EffortEstimationService()
mvp_service = MVPGeneratorService(effort_service)

# In-memory storage (enhanced)
projects: Dict[str, EnhancedProject] = {}
project_features: Dict[str, List[EnhancedFeature]] = defaultdict(list)
url_contexts: Dict[str, Dict[str, Any]] = {}
mvp_definitions: Dict[str, MVPDefinition] = {}

# Request/Response models for API
class ProjectCreateRequest(BaseModel):
    name: str
    description: str
    industry: str
    target_users: str
    reference_url: Optional[HttpUrl] = None
    timeline_weeks: Optional[int] = None
    budget_range: Optional[str] = None
    team_size: Optional[int] = None
    tech_stack: Optional[Dict[str, List[str]]] = None
    team_experience: Optional[str] = "intermediate"
    project_goals: Optional[List[str]] = []

class FeatureRequest(BaseModel):
    name: str
    description: str
    user_story: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    priority: str = "medium"

class FeatureValidationResponse(BaseModel):
    feature: FeatureRequest
    result: ValidationResult
    effort_estimate: EffortEstimate
    timestamp: str
    processing_time: float

def mock_analyze_feature_enhanced(
    feature_description: str, 
    feature_name: str, 
    project: Optional[EnhancedProject] = None,
    context: Optional[Dict[str, Any]] = None
) -> dict:
    """Enhanced MVP analysis using research-backed methodologies."""
    
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Research-based MVP evaluation framework
    # Based on Eric Ries' Lean Startup, Steve Blank's Customer Development, and Y Combinator guidelines
    
    # 1. LEAN STARTUP METRICS - Build-Measure-Learn cycle readiness
    lean_startup_score = calculate_lean_startup_score(feature_description, feature_name)
    
    # 2. CUSTOMER DEVELOPMENT SCORE - Problem-solution fit validation
    customer_dev_score = calculate_customer_development_score(feature_description, feature_name, project)
    
    # 3. KANO MODEL ANALYSIS - Feature necessity classification
    kano_classification = classify_feature_kano_model(feature_description, feature_name, project)
    
    # 4. RICE PRIORITIZATION - Reach, Impact, Confidence, Effort
    rice_score = calculate_rice_score(feature_description, feature_name, project, context)
    
    # Enhanced complexity analysis with research-backed factors
    complexity_keywords = {
        # High complexity (8-10) - Avoid in MVP
        'machine learning': 10, 'ai': 9, 'blockchain': 10, 'real-time': 8,
        'recommendation': 9, 'personalization': 8, 'microservices': 9,
        'enterprise': 9, 'sophisticated': 8, 'advanced analytics': 10,
        
        # Medium complexity (5-7) - Consider carefully
        'analytics': 6, 'integration': 6, 'api': 5, 'advanced': 6,
        'complex': 7, 'custom': 6, 'scalable': 6, 'reporting': 6,
        
        # Low complexity (1-4) - MVP friendly
        'secure': 3, 'compliant': 4, 'basic': 2, 'simple': 1,
        'standard': 2, 'template': 2, 'existing': 2
    }
    
    # Research-backed MVP keywords with validated importance scores
    mvp_keywords = {
        # Core MVP features (9-10) - Essential for validation
        'authentication': 10, 'login': 10, 'register': 9, 'core': 10,
        'essential': 10, 'critical': 10, 'basic': 9, 'fundamental': 10,
        
        # High value MVP features (7-8) - Important for user journey
        'dashboard': 8, 'profile': 7, 'user': 8, 'main': 8, 'primary': 8,
        'crud': 8, 'create': 8, 'view': 8, 'manage': 7, 'key': 8,
        
        # Medium value features (5-6) - Nice to have
        'search': 6, 'form': 6, 'edit': 6, 'delete': 6, 'list': 7,
        'notification': 5, 'settings': 5, 'preferences': 5
    }
    
    # Calculate base scores
    complexity_score = 3
    for keyword, score in complexity_keywords.items():
        if keyword in description_lower or keyword in name_lower:
            complexity_score = max(complexity_score, score)
            break
    
    mvp_score = 5
    for keyword, score in mvp_keywords.items():
        if keyword in description_lower or keyword in name_lower:
            mvp_score = max(mvp_score, score)
            break
    
    # Tech stack context adjustments
    if project and project.tech_stack:
        # React bonus for UI features
        if any("React" in str(tech) for tech in project.tech_stack.frontend):
            if any(ui_word in description_lower for ui_word in ['dashboard', 'interface', 'form', 'component']):
                complexity_score = max(1, complexity_score - 1)
        
        # Database complexity
        if any("Firebase" in str(tech) for tech in project.tech_stack.database):
            if 'auth' in description_lower:
                complexity_score = max(1, complexity_score - 2)  # Firebase Auth is easy
        
        # Integration services
        if any("Stripe" in str(tech) for tech in project.tech_stack.integrations):
            if 'payment' in description_lower:
                complexity_score = max(1, complexity_score - 1)
    
    # Industry context
    if project:
        if project.industry == "E-COMMERCE" and any(word in description_lower for word in ['shop', 'cart', 'checkout', 'payment']):
            mvp_score += 1
        elif project.industry == "FINTECH" and 'payment' in description_lower:
            mvp_score += 2
            complexity_score += 1  # Financial features need more security
    
    # Team experience impact
    if project and project.team_experience:
        if project.team_experience == TeamExperience.BEGINNER:
            complexity_score += 1
        elif project.team_experience == TeamExperience.EXPERT:
            complexity_score = max(1, complexity_score - 1)
    
    # Cap scores
    complexity_score = min(complexity_score, 10)
    mvp_score = min(mvp_score, 10)
    
    # User value based on description quality and industry fit
    user_value_score = min(6 + len(feature_description) // 50, 10)
    if project and project.industry in ["E-COMMERCE", "FINTECH", "HEALTHCARE"]:
        user_value_score += 1
    user_value_score = min(user_value_score, 10)
    
    # Overall score calculation
    overall_score = (mvp_score * 0.4 + user_value_score * 0.3 + (10 - complexity_score) * 0.3)
    
    # Decision logic
    if mvp_score >= 7 and complexity_score <= 6:
        decision = "ACCEPT"
        rationale = f"Excellent MVP fit with high value ({user_value_score}/10) and manageable complexity ({complexity_score}/10)."
        alternatives = []
    elif complexity_score >= 8:
        decision = "MODIFY"
        rationale = f"High complexity ({complexity_score}/10) for MVP. Consider simplifying or phasing implementation."
        alternatives = [
            "Start with basic version and iterate",
            "Use third-party services to reduce complexity",
            "Break into smaller, simpler features",
            "Consider no-code/low-code solutions"
        ]
    elif mvp_score <= 4:
        decision = "DEFER"
        rationale = f"Low MVP priority ({mvp_score}/10). Focus on core features first."
        alternatives = [
            "Add to post-MVP roadmap",
            "Validate with user feedback first",
            "Consider as enhancement feature",
            "Combine with related core features"
        ]
    else:
        decision = "ACCEPT"
        rationale = f"Good balance of value ({user_value_score}/10) and complexity ({complexity_score}/10) for MVP."
        alternatives = []
    
    # Timeline estimation based on complexity and tech stack (in days)
    base_days = {1: 3, 2: 7, 3: 10, 4: 14, 5: 21, 6: 28, 7: 42, 8: 56, 9: 84, 10: 112}
    timeline_days = base_days.get(complexity_score, 28)
    
    # Tech stack adjustments
    if project and project.tech_stack:
        total_tech = (len(project.tech_stack.frontend) + len(project.tech_stack.backend) + 
                     len(project.tech_stack.database) + len(project.tech_stack.integrations))
        if total_tech > 6:
            timeline_days = int(timeline_days * 1.2)
    
    timeline_impact = f"{timeline_days} days"
    
    return {
        "core_mvp_score": mvp_score,
        "complexity_score": complexity_score,
        "user_value_score": user_value_score,
        "overall_score": round(overall_score, 2),
        "decision": decision,
        "rationale": rationale,
        "alternatives": alternatives,
        "timeline_impact": timeline_impact,
        "dependencies": ["Authentication system"] if "login" in description_lower or "user" in description_lower else []
    }

def mock_analyze_url_enhanced(url: HttpUrl) -> Dict[str, Any]:
    """Enhanced URL analysis with deeper insights."""
    url_str = str(url).lower()
    
    # Enhanced pattern matching
    if any(pattern in url_str for pattern in ['shop', 'store', 'ecommerce', 'commerce', 'buy', 'sell']):
        return {
            "url": url,
            "title": "E-commerce Platform Analysis",
            "description": "Comprehensive e-commerce solution with modern features",
            "extracted_features": [
                "Product catalog with categories", "Advanced search and filtering", 
                "Shopping cart with persistence", "Multi-step checkout process",
                "Payment processing (multiple methods)", "User account management",
                "Order tracking and history", "Inventory management",
                "Customer reviews and ratings", "Wishlist functionality"
            ],
            "tech_stack": ["React", "Node.js", "PostgreSQL", "Stripe", "AWS"],
            "ui_patterns": ["responsive grid", "modal dialogs", "progressive forms", "infinite scroll"],
            "business_model": "ecommerce",
            "target_audience": "online shoppers and merchants",
            "key_functionality": [
                "Browse and search products", "Secure checkout process",
                "Account management", "Order tracking", "Payment processing"
            ],
            "competitive_advantages": [
                "Mobile-first design", "Fast checkout process", 
                "Comprehensive product search", "Secure payment handling"
            ],
            "extracted_at": datetime.now()
        }
    
    elif any(pattern in url_str for pattern in ['github', 'gitlab', 'code', 'dev']):
        return {
            "url": url,
            "title": "Developer Platform Analysis",
            "description": "Code collaboration and project management platform",
            "extracted_features": [
                "Git repository management", "Issue tracking system",
                "Pull request workflow", "CI/CD pipeline integration",
                "Team collaboration tools", "Code review system",
                "Project wikis and documentation", "Release management"
            ],
            "tech_stack": ["React", "Ruby on Rails", "PostgreSQL", "Redis", "Docker"],
            "ui_patterns": ["tabbed interface", "code syntax highlighting", "activity feeds", "notification system"],
            "business_model": "saas",
            "target_audience": "developers and development teams",
            "key_functionality": [
                "Version control", "Code collaboration", "Project management",
                "Automated testing", "Documentation"
            ],
            "competitive_advantages": [
                "Integrated development workflow", "Strong community features",
                "Extensive API ecosystem", "Enterprise security"
            ],
            "extracted_at": datetime.now()
        }
    
    elif any(pattern in url_str for pattern in ['social', 'community', 'connect', 'network']):
        return {
            "url": url,
            "title": "Social Platform Analysis",
            "description": "Community-driven social networking platform",
            "extracted_features": [
                "User profiles and customization", "News feed with algorithms",
                "Real-time messaging system", "Content sharing (text, images, video)",
                "Social connections (friends, followers)", "Groups and communities",
                "Event creation and management", "Privacy controls"
            ],
            "tech_stack": ["React", "Node.js", "MongoDB", "Socket.io", "AWS"],
            "ui_patterns": ["infinite scroll feed", "real-time notifications", "modal overlays", "responsive cards"],
            "business_model": "social",
            "target_audience": "social media users and communities",
            "key_functionality": [
                "Connect with others", "Share content", "Real-time communication",
                "Discover communities", "Event participation"
            ],
            "competitive_advantages": [
                "Real-time interactions", "Personalized content feed",
                "Strong privacy controls", "Community-focused features"
            ],
            "extracted_at": datetime.now()
        }
    
    else:
        return {
            "url": url,
            "title": "General Platform Analysis",
            "description": "Multi-purpose web application",
            "extracted_features": [
                "User authentication", "Dashboard interface",
                "Data management", "Search functionality",
                "User profiles", "Settings management"
            ],
            "tech_stack": ["React", "Node.js", "PostgreSQL"],
            "ui_patterns": ["navigation menu", "form interfaces", "data tables"],
            "business_model": "saas",
            "target_audience": "general users",
            "key_functionality": [
                "User management", "Data processing", "Interface interaction"
            ],
            "competitive_advantages": [
                "Clean interface", "Reliable functionality"
            ],
            "extracted_at": datetime.now()
        }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Ultimate MVP Generation Agent",
        "version": "3.0.0",
        "docs": "/docs",
        "features": [
            "Tech Stack-Aware Effort Estimation",
            "MVP Generation with Value Propositions",
            "Enhanced URL Context Analysis",
            "Dynamic MVP Re-evaluation",
            "Comprehensive Project Analytics"
        ]
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "effort_estimation": "active",
            "mvp_generation": "active",
            "url_analysis": "active"
        }
    }

@app.post("/api/v1/projects")
async def create_project(project_data: ProjectCreateRequest):
    """Create enhanced project with tech stack."""
    project_id = str(uuid.uuid4())
    
    # Parse tech stack
    tech_stack = ProjectTechStack()
    if project_data.tech_stack:
        tech_stack.frontend = [TechStack(t) for t in project_data.tech_stack.get('frontend', [])]
        tech_stack.backend = [TechStack(t) for t in project_data.tech_stack.get('backend', [])]
        tech_stack.database = [TechStack(t) for t in project_data.tech_stack.get('database', [])]
        tech_stack.cloud = [TechStack(t) for t in project_data.tech_stack.get('cloud', [])]
        tech_stack.integrations = [TechStack(t) for t in project_data.tech_stack.get('integrations', [])]
    
    # URL analysis
    url_context = None
    if project_data.reference_url:
        try:
            url_context = mock_analyze_url_enhanced(project_data.reference_url)
            url_contexts[project_id] = url_context
        except Exception as e:
            logger.error(f"URL analysis failed: {str(e)}")
    
    # Create enhanced project
    project = EnhancedProject(
        id=project_id,
        name=project_data.name,
        description=project_data.description,
        industry=project_data.industry,
        target_users=project_data.target_users,
        reference_url=project_data.reference_url,
        timeline_weeks=project_data.timeline_weeks,
        budget_range=project_data.budget_range,
        team_size=project_data.team_size,
        tech_stack=tech_stack,
        team_experience=TeamExperience(project_data.team_experience),
        project_goals=project_data.project_goals or [],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    projects[project_id] = project
    logger.info(f"Created enhanced project: {project.name} (ID: {project_id})")
    
    return project

@app.post("/api/v1/projects/{project_id}/features")
async def add_feature_to_project(project_id: str, feature_request: FeatureRequest):
    """Add feature with enhanced validation and effort estimation."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    start_time = time.time()
    
    # Enhanced validation with project context
    validation_analysis = mock_analyze_feature_enhanced(
        feature_request.description,
        feature_request.name,
        project,
        {"existing_features": project_features[project_id]}
    )
    
    # Create validation result
    score = ValidationScore(
        core_mvp_score=validation_analysis["core_mvp_score"],
        complexity_score=validation_analysis["complexity_score"],
        user_value_score=validation_analysis["user_value_score"],
        overall_score=validation_analysis["overall_score"]
    )
    
    validation_result = ValidationResult(
        decision=ValidationDecision(validation_analysis["decision"]),
        score=score,
        rationale=validation_analysis["rationale"],
        alternatives=validation_analysis["alternatives"],
        timeline_impact=validation_analysis["timeline_impact"],
        dependencies=validation_analysis["dependencies"],
        confidence=0.95
    )
    
    # Create enhanced feature
    feature_id = str(uuid.uuid4())
    enhanced_feature = EnhancedFeature(
        id=feature_id,
        project_id=project_id,
        feature_name=feature_request.name,
        feature_description=feature_request.description,
        user_story=feature_request.user_story,
        acceptance_criteria=feature_request.acceptance_criteria or [],
        priority=feature_request.priority,
        status="APPROVED" if validation_result.decision == ValidationDecision.ACCEPT else "PENDING",
        estimated_weeks=float(validation_analysis["timeline_impact"].split()[0]) / 7 if "days" in validation_analysis["timeline_impact"] else float(validation_analysis["timeline_impact"].split()[0]),
        validation_result=validation_result.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Calculate effort estimate
    effort_estimate = effort_service.estimate_feature_effort(enhanced_feature, project)
    enhanced_feature.effort_estimate = effort_estimate
    
    # Add to project
    project_features[project_id].append(enhanced_feature)
    
    # Update project stats
    project.total_features = len(project_features[project_id])
    project.approved_features = sum(1 for f in project_features[project_id] if f.status == "APPROVED")
    project.updated_at = datetime.now()
    
    processing_time = time.time() - start_time
    
    return FeatureValidationResponse(
        feature=feature_request,
        result=validation_result,
        effort_estimate=effort_estimate,
        timestamp=datetime.now().isoformat(),
        processing_time=processing_time
    )

@app.post("/api/v1/projects/{project_id}/features/{feature_id}/generate-user-story")
async def generate_user_story(project_id: str, feature_id: str):
    """Generate user story for a feature using AI."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    features = project_features[project_id]
    
    # Find the feature
    feature_to_update = None
    for feature in features:
        if feature.id == feature_id:
            feature_to_update = feature
            break
    
    if not feature_to_update:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    # Generate user story using AI-like logic
    user_story = generate_ai_user_story(
        feature_to_update.feature_name,
        feature_to_update.feature_description,
        project
    )
    
    # Update feature with generated user story
    feature_to_update.user_story = user_story
    feature_to_update.updated_at = datetime.now()
    
    logger.info(f"Generated user story for feature {feature_id} in project {project_id}")
    
    return {
        "feature_id": feature_id,
        "user_story": user_story,
        "timestamp": datetime.now().isoformat(),
        "message": "User story generated successfully"
    }

def generate_ai_user_story(feature_name: str, feature_description: str, project: EnhancedProject) -> str:
    """Generate user story using AI-like logic based on feature and project context."""
    
    # Determine user type based on project context
    target_users = project.target_users.lower()
    
    if "business" in target_users or "owner" in target_users:
        user_type = "business owner"
    elif "customer" in target_users or "shopper" in target_users:
        user_type = "customer"
    elif "developer" in target_users or "technical" in target_users:
        user_type = "developer"
    elif "manager" in target_users:
        user_type = "project manager"
    elif "team" in target_users:
        user_type = "team member"
    else:
        user_type = "user"
    
    # Determine action based on feature name and description
    feature_lower = feature_name.lower()
    description_lower = feature_description.lower()
    
    if "auth" in feature_lower or "login" in feature_lower:
        action = "securely log into the platform"
        benefit = "access my personal account and data"
    elif "dashboard" in feature_lower:
        action = "view a comprehensive dashboard"
        benefit = "quickly understand the current status and key metrics"
    elif "search" in feature_lower:
        action = "search for relevant content"
        benefit = "quickly find what I'm looking for"
    elif "profile" in feature_lower:
        action = "manage my profile information"
        benefit = "keep my information up-to-date and personalized"
    elif "payment" in feature_lower or "checkout" in feature_lower:
        action = "complete secure transactions"
        benefit = "purchase products/services safely and efficiently"
    elif "notification" in feature_lower:
        action = "receive timely notifications"
        benefit = "stay informed about important updates"
    elif "report" in feature_lower or "analytics" in feature_lower:
        action = "generate detailed reports"
        benefit = "make data-driven decisions"
    elif "message" in feature_lower or "chat" in feature_lower:
        action = "communicate with other users"
        benefit = "collaborate effectively and stay connected"
    elif "upload" in feature_lower or "file" in feature_lower:
        action = "upload and manage files"
        benefit = "organize and share my documents efficiently"
    else:
        # Generic action based on description
        if "create" in description_lower:
            action = f"create and manage {feature_name.lower()}"
            benefit = "organize my work more effectively"
        elif "track" in description_lower:
            action = f"track {feature_name.lower()}"
            benefit = "monitor progress and stay organized"
        elif "manage" in description_lower:
            action = f"manage {feature_name.lower()}"
            benefit = "have better control over my workflow"
        else:
            action = f"use {feature_name.lower()}"
            benefit = "accomplish my goals more efficiently"
    
    # Industry-specific benefit adjustments
    if project.industry == "E-COMMERCE":
        if "payment" in feature_lower:
            benefit = "complete purchases quickly and securely"
        elif "product" in feature_lower:
            benefit = "find and purchase the right products"
    elif project.industry == "FINTECH":
        if "payment" in feature_lower:
            benefit = "manage my finances securely"
        elif "account" in feature_lower:
            benefit = "have full control over my financial data"
    elif project.industry == "HEALTHCARE":
        if "record" in feature_lower:
            benefit = "maintain accurate health records"
        elif "appointment" in feature_lower:
            benefit = "manage my healthcare appointments efficiently"
    elif project.industry == "PRODUCTIVITY":
        if "task" in feature_lower:
            benefit = "stay organized and meet deadlines"
        elif "team" in feature_lower:
            benefit = "collaborate effectively with my team"
    
    # Construct user story
    user_story = f"As a {user_type}, I want to {action} so that I can {benefit}."
    
    return user_story

def calculate_lean_startup_score(feature_description: str, feature_name: str) -> float:
    """Calculate Lean Startup methodology score - Build-Measure-Learn readiness."""
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Build readiness - How easy is it to build?
    build_keywords = ['simple', 'basic', 'standard', 'template', 'existing']
    build_score = 5
    for keyword in build_keywords:
        if keyword in description_lower or keyword in name_lower:
            build_score += 2
            break
    
    # Measure readiness - Can we measure user behavior?
    measure_keywords = ['analytics', 'tracking', 'metrics', 'feedback', 'usage']
    measure_score = 5
    for keyword in measure_keywords:
        if keyword in description_lower:
            measure_score += 2
            break
    
    # Learn readiness - Will this teach us about users?
    learn_keywords = ['user', 'customer', 'behavior', 'preference', 'interaction']
    learn_score = 5
    for keyword in learn_keywords:
        if keyword in description_lower:
            learn_score += 2
            break
    
    return min((build_score + measure_score + learn_score) / 3, 10)

def calculate_customer_development_score(feature_description: str, feature_name: str, project: Optional[EnhancedProject]) -> float:
    """Calculate Customer Development score - Problem-solution fit validation."""
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Problem validation - Does this address a real problem?
    problem_keywords = ['problem', 'pain', 'issue', 'challenge', 'difficulty', 'frustration']
    problem_score = 5
    for keyword in problem_keywords:
        if keyword in description_lower:
            problem_score += 1
    
    # Solution fit - How well does this solve the problem?
    solution_keywords = ['solve', 'fix', 'improve', 'optimize', 'streamline', 'simplify']
    solution_score = 5
    for keyword in solution_keywords:
        if keyword in description_lower:
            solution_score += 1
    
    # Customer validation - Can customers validate this?
    validation_keywords = ['test', 'validate', 'feedback', 'interview', 'survey']
    validation_score = 5
    if any(keyword in description_lower for keyword in validation_keywords):
        validation_score += 2
    
    return min((problem_score + solution_score + validation_score) / 3, 10)

def classify_feature_kano_model(feature_description: str, feature_name: str, project: Optional[EnhancedProject]) -> str:
    """Classify feature using Kano Model - Must-have, Performance, or Delighter."""
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Must-have features (Basic expectations)
    must_have_keywords = ['authentication', 'login', 'security', 'basic', 'core', 'essential']
    if any(keyword in description_lower or keyword in name_lower for keyword in must_have_keywords):
        return "MUST_HAVE"
    
    # Performance features (More is better)
    performance_keywords = ['speed', 'performance', 'efficiency', 'optimization', 'fast']
    if any(keyword in description_lower for keyword in performance_keywords):
        return "PERFORMANCE"
    
    # Delighter features (Unexpected value)
    delighter_keywords = ['ai', 'machine learning', 'personalization', 'recommendation', 'smart']
    if any(keyword in description_lower for keyword in delighter_keywords):
        return "DELIGHTER"
    
    return "PERFORMANCE"  # Default classification

def calculate_rice_score(feature_description: str, feature_name: str, project: Optional[EnhancedProject], context: Optional[Dict[str, Any]]) -> float:
    """Calculate RICE score - Reach, Impact, Confidence, Effort."""
    description_lower = feature_description.lower()
    name_lower = feature_name.lower()
    
    # Reach - How many users will this affect?
    reach_keywords = ['all users', 'every user', 'user base', 'customers']
    reach_score = 5  # Default medium reach
    if any(keyword in description_lower for keyword in reach_keywords):
        reach_score = 8
    elif any(keyword in description_lower for keyword in ['some users', 'specific users']):
        reach_score = 3
    
    # Impact - How much will this impact each user?
    impact_keywords = ['critical', 'essential', 'important', 'significant', 'major']
    impact_score = 5  # Default medium impact
    if any(keyword in description_lower or keyword in name_lower for keyword in impact_keywords):
        impact_score = 8
    elif any(keyword in description_lower for keyword in ['minor', 'small', 'slight']):
        impact_score = 2
    
    # Confidence - How confident are we in our estimates?
    confidence_score = 7  # Default high confidence for well-defined features
    if len(feature_description) < 50:  # Short descriptions = lower confidence
        confidence_score = 5
    elif len(feature_description) > 200:  # Detailed descriptions = higher confidence
        confidence_score = 9
    
    # Effort - How much work is required? (inverse score - lower effort = higher score)
    effort_keywords = ['complex', 'advanced', 'sophisticated', 'integration']
    effort_score = 7  # Default medium effort
    if any(keyword in description_lower for keyword in effort_keywords):
        effort_score = 3  # High effort = low score
    elif any(keyword in description_lower for keyword in ['simple', 'basic', 'standard']):
        effort_score = 9  # Low effort = high score
    
    # RICE = (Reach * Impact * Confidence) / Effort
    rice_score = (reach_score * impact_score * confidence_score) / (11 - effort_score)  # Convert effort to divisor
    return min(rice_score / 50, 10)  # Normalize to 0-10 scale

@app.put("/api/v1/projects/{project_id}/features/{feature_id}/re-evaluate")
async def re_evaluate_feature(project_id: str, feature_id: str):
    """Re-evaluate a feature with updated project context."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    features = project_features[project_id]
    
    # Find the feature to re-evaluate
    feature_to_update = None
    for feature in features:
        if feature.id == feature_id:
            feature_to_update = feature
            break
    
    if not feature_to_update:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    start_time = time.time()
    
    # Re-run validation with current project context
    validation_analysis = mock_analyze_feature_enhanced(
        feature_to_update.feature_description,
        feature_to_update.feature_name,
        project,
        {"existing_features": features}
    )
    
    # Update validation result
    score = ValidationScore(
        core_mvp_score=validation_analysis["core_mvp_score"],
        complexity_score=validation_analysis["complexity_score"],
        user_value_score=validation_analysis["user_value_score"],
        overall_score=validation_analysis["overall_score"]
    )
    
    validation_result = ValidationResult(
        decision=ValidationDecision(validation_analysis["decision"]),
        score=score,
        rationale=validation_analysis["rationale"],
        alternatives=validation_analysis["alternatives"],
        timeline_impact=validation_analysis["timeline_impact"],
        dependencies=validation_analysis["dependencies"],
        confidence=0.95
    )
    
    # Update feature
    feature_to_update.validation_result = validation_result.dict()
    feature_to_update.status = "APPROVED" if validation_result.decision == ValidationDecision.ACCEPT else "PENDING"
    feature_to_update.estimated_weeks = float(validation_analysis["timeline_impact"].split()[0]) / 7 if "days" in validation_analysis["timeline_impact"] else float(validation_analysis["timeline_impact"].split()[0])
    feature_to_update.updated_at = datetime.now()
    
    # Recalculate effort estimate
    effort_estimate = effort_service.estimate_feature_effort(feature_to_update, project)
    feature_to_update.effort_estimate = effort_estimate
    
    # Update project stats
    project.approved_features = sum(1 for f in features if f.status == "APPROVED")
    project.updated_at = datetime.now()
    
    processing_time = time.time() - start_time
    
    logger.info(f"Re-evaluated feature {feature_id} for project {project_id}")
    
    return {
        "feature": feature_to_update,
        "validation_result": validation_result,
        "effort_estimate": effort_estimate,
        "timestamp": datetime.now().isoformat(),
        "processing_time": processing_time,
        "message": "Feature re-evaluated successfully"
    }

@app.post("/api/v1/projects/{project_id}/generate-mvp")
async def generate_mvp(project_id: str, request: Optional[Dict[str, Any]] = None):
    """Generate comprehensive MVP with value proposition."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    features = project_features[project_id]
    url_context = url_contexts.get(project_id)
    
    # Create MVPGenerationRequest with project_id
    mvp_request = MVPGenerationRequest(
        project_id=project_id,
        include_pending_features=request.get("include_pending_features", False) if request else False,
        max_timeline_weeks=request.get("max_timeline_weeks") if request else None,
        max_effort_hours=request.get("max_effort_hours") if request else None,
        priority_threshold=request.get("priority_threshold") if request else None
    )
    
    # Generate MVP
    mvp_definition = await mvp_service.generate_mvp(mvp_request, project, features, url_context)
    
    # Store MVP definition
    mvp_definitions[project_id] = mvp_definition
    project.mvp_definition = mvp_definition
    project.mvp_status = MVPStatus.DEFINED
    project.updated_at = datetime.now()
    
    logger.info(f"Generated MVP for project {project_id} with {len(mvp_definition.core_features)} features")
    
    return mvp_definition

@app.get("/api/v1/projects/{project_id}")
async def get_project_enhanced(project_id: str):
    """Get enhanced project with complete analytics."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    features = project_features[project_id]
    url_context = url_contexts.get(project_id)
    mvp_definition = mvp_definitions.get(project_id)
    
    # Generate enhanced analytics
    analytics = generate_enhanced_analytics(project, features, url_context, mvp_definition)
    
    return {
        "project": project,
        "features": features,
        "analytics": analytics,
        "url_context": url_context,
        "mvp_definition": mvp_definition
    }

@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and all its associated data."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    
    # Clean up all associated data
    del projects[project_id]
    if project_id in project_features:
        del project_features[project_id]
    if project_id in url_contexts:
        del url_contexts[project_id]
    if project_id in mvp_definitions:
        del mvp_definitions[project_id]
    
    logger.info(f"Deleted project: {project.name} (ID: {project_id})")
    
    return {
        "message": "Project deleted successfully",
        "project_id": project_id,
        "project_name": project.name,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/projects")
async def list_projects():
    """List all projects with summary."""
    project_summaries = []
    
    for project in projects.values():
        features = project_features[project.id]
        summary = {
            "project": project,
            "feature_count": len(features),
            "approved_features": sum(1 for f in features if f.status == "APPROVED"),
            "mvp_status": project.mvp_status,
            "has_url_context": project.id in url_contexts
        }
        project_summaries.append(summary)
    
    return {
        "projects": project_summaries,
        "total": len(projects)
    }

@app.post("/api/v1/analyze-url")
async def analyze_url_enhanced(request: dict):
    """Enhanced URL analysis."""
    url = request.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        context = mock_analyze_url_enhanced(url)
        return {
            "url": url,
            "context": context,
            "recommendations": generate_url_recommendations(context),
            "integration_suggestions": generate_integration_suggestions(context),
            "tech_stack_suggestions": suggest_tech_stack(context)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to analyze URL: {str(e)}")

def generate_enhanced_analytics(
    project: EnhancedProject, 
    features: List[EnhancedFeature],
    url_context: Optional[Dict[str, Any]] = None,
    mvp_definition: Optional[MVPDefinition] = None
) -> ProjectAnalyticsEnhanced:
    """Generate comprehensive project analytics."""
    
    # Feature breakdown
    feature_breakdown = defaultdict(int)
    priority_breakdown = defaultdict(int)
    
    for feature in features:
        feature_breakdown[feature.status] += 1
        priority_breakdown[feature.priority] += 1
    
    # Effort calculations
    total_effort_hours = sum(f.effort_estimate.final_estimate_hours for f in features if f.effort_estimate)
    total_timeline = sum(f.estimated_weeks or 0 for f in features if f.status == "APPROVED")
    
    # Tech stack complexity
    tech_complexity = calculate_tech_stack_complexity(project.tech_stack)
    
    # Team velocity
    team_velocity = effort_service._calculate_team_velocity(project)
    
    # MVP insights
    mvp_insights = None
    value_prop_summary = None
    if mvp_definition:
        mvp_insights = {
            "core_features_count": len(mvp_definition.core_features),
            "estimated_timeline": mvp_definition.estimated_timeline_weeks,
            "confidence_score": mvp_definition.value_proposition.confidence_score,
            "competitive_advantages": len(mvp_definition.value_proposition.competitive_advantages)
        }
        value_prop_summary = mvp_definition.value_proposition.headline
    
    return ProjectAnalyticsEnhanced(
        project_id=project.id,
        total_features=len(features),
        feature_breakdown=dict(feature_breakdown),
        priority_breakdown=dict(priority_breakdown),
        estimated_timeline=total_timeline,
        estimated_effort_hours=total_effort_hours,
        complexity_score=sum(f.validation_result.get('score', {}).get('complexity_score', 5) for f in features if f.validation_result) / max(len(features), 1),
        mvp_readiness=calculate_mvp_readiness(features),
        tech_stack_complexity=tech_complexity,
        team_velocity_estimate=team_velocity,
        recommendations=generate_project_recommendations(project, features, url_context),
        risk_factors=identify_project_risks(project, features),
        suggested_phases=suggest_development_phases(features),
        url_context_insights=generate_url_insights(url_context, features) if url_context else None,
        mvp_insights=mvp_insights,
        value_proposition_summary=value_prop_summary
    )

def calculate_tech_stack_complexity(tech_stack: ProjectTechStack) -> float:
    """Calculate tech stack complexity score."""
    total_technologies = (
        len(tech_stack.frontend) + len(tech_stack.backend) + 
        len(tech_stack.database) + len(tech_stack.cloud) + 
        len(tech_stack.integrations)
    )
    
    # Base complexity
    complexity = min(total_technologies / 10, 1.0) * 5  # Scale to 0-5
    
    # Complexity penalties for specific combinations
    if len(tech_stack.frontend) > 1:
        complexity += 0.5  # Multiple frontend frameworks
    
    if len(tech_stack.backend) > 1:
        complexity += 0.5  # Multiple backend frameworks
    
    return min(complexity, 10.0)

def calculate_mvp_readiness(features: List[EnhancedFeature]) -> float:
    """Calculate MVP readiness score."""
    if not features:
        return 0.0
    
    approved_features = [f for f in features if f.status == "APPROVED"]
    high_priority_features = [f for f in features if f.priority == "high"]
    
    if not approved_features:
        return 0.0
    
    # Readiness factors
    approval_ratio = len(approved_features) / len(features)
    priority_coverage = len([f for f in approved_features if f.priority == "high"]) / max(len(high_priority_features), 1)
    feature_quality = sum(f.validation_result.get('score', {}).get('overall_score', 5) for f in approved_features) / len(approved_features)
    
    readiness = (approval_ratio * 0.4 + priority_coverage * 0.3 + feature_quality / 10 * 0.3) * 10
    return min(readiness, 10.0)

def generate_project_recommendations(
    project: EnhancedProject, 
    features: List[EnhancedFeature],
    url_context: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Generate enhanced project recommendations."""
    recommendations = []
    
    # Feature recommendations
    approved_count = sum(1 for f in features if f.status == "APPROVED")
    if approved_count < 3:
        recommendations.append("Add more core features to create a viable MVP")
    
    # Tech stack recommendations
    if not project.tech_stack.frontend:
        recommendations.append("Define frontend technology stack for better effort estimation")
    
    if not project.tech_stack.database:
        recommendations.append("Choose database technology based on data requirements")
    
    # Timeline recommendations
    total_effort = sum(f.effort_estimate.final_estimate_hours for f in features if f.effort_estimate)
    if total_effort > 1000:  # 25 weeks for single developer
        recommendations.append("Consider reducing scope or increasing team size")
    
    # URL context recommendations
    if url_context:
        if url_context.get('business_model') == 'ecommerce' and project.industry != "E-COMMERCE":
            recommendations.append("Consider aligning project industry with reference system")
    
    return recommendations

def identify_project_risks(project: EnhancedProject, features: List[EnhancedFeature]) -> List[str]:
    """Identify enhanced project risks."""
    risks = []
    
    # Complexity risks
    high_complexity_features = [
        f for f in features 
        if f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) > 7
    ]
    
    if len(high_complexity_features) > len(features) * 0.3:
        risks.append("High number of complex features may impact timeline and budget")
    
    # Tech stack risks
    tech_count = (len(project.tech_stack.frontend) + len(project.tech_stack.backend) + 
                 len(project.tech_stack.database) + len(project.tech_stack.integrations))
    
    if tech_count > 8:
        risks.append("Complex tech stack may increase integration challenges and learning curve")
    
    # Team risks
    if project.team_experience == TeamExperience.BEGINNER and tech_count > 4:
        risks.append("Inexperienced team with complex tech stack may face significant challenges")
    
    # Timeline risks
    if project.timeline_weeks:
        total_effort_weeks = sum(f.effort_estimate.final_estimate_weeks for f in features if f.effort_estimate)
        if total_effort_weeks > project.timeline_weeks:
            risks.append(f"Estimated effort ({total_effort_weeks:.1f} weeks) exceeds timeline ({project.timeline_weeks} weeks)")
    
    return risks

def suggest_development_phases(features: List[EnhancedFeature]) -> List[Dict[str, Any]]:
    """Suggest enhanced development phases."""
    phases = []
    
    # Phase 1: Core MVP (high priority, approved, low complexity)
    core_features = [
        f for f in features 
        if (f.status == "APPROVED" and f.priority == "high" and 
            f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) <= 6)
    ]
    
    if core_features:
        phases.append({
            "phase": 1,
            "name": "Core MVP",
            "features": [f.feature_name for f in core_features],
            "estimated_weeks": sum(f.estimated_weeks or 0 for f in core_features),
            "description": "Essential high-priority features with low complexity"
        })
    
    # Phase 2: Enhancement features (medium priority, approved)
    enhancement_features = [
        f for f in features 
        if (f.status == "APPROVED" and f.priority == "medium" and 
            f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) <= 7)
    ]
    
    if enhancement_features:
        phases.append({
            "phase": 2,
            "name": "Feature Enhancement",
            "features": [f.feature_name for f in enhancement_features],
            "estimated_weeks": sum(f.estimated_weeks or 0 for f in enhancement_features),
            "description": "Medium-priority features to improve user experience"
        })
    
    # Phase 3: Advanced features (complex or low priority)
    advanced_features = [
        f for f in features 
        if (f.status == "APPROVED" and 
            (f.priority == "low" or 
             (f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) > 7)))
    ]
    
    if advanced_features:
        phases.append({
            "phase": 3,
            "name": "Advanced Features",
            "features": [f.feature_name for f in advanced_features],
            "estimated_weeks": sum(f.estimated_weeks or 0 for f in advanced_features),
            "description": "Complex or nice-to-have features for future iterations"
        })
    
    return phases

def generate_url_recommendations(context: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on URL analysis."""
    recommendations = []
    
    business_model = context.get('business_model', '')
    
    if business_model == 'ecommerce':
        recommendations.extend([
            "Focus on conversion optimization features",
            "Implement robust inventory management",
            "Prioritize mobile-first checkout experience",
            "Consider multiple payment method support"
        ])
    elif business_model == 'saas':
        recommendations.extend([
            "Implement user onboarding flow",
            "Focus on core workflow features",
            "Add usage analytics and reporting",
            "Consider freemium model features"
        ])
    elif business_model == 'social':
        recommendations.extend([
            "Prioritize user engagement features",
            "Implement strong privacy controls",
            "Focus on community building tools",
            "Add content moderation capabilities"
        ])
    
    # Tech stack recommendations
    tech_stack = context.get('tech_stack', [])
    if 'React' in tech_stack:
        recommendations.append("Use React for frontend consistency with reference system")
    if 'Node.js' in tech_stack:
        recommendations.append("Consider Node.js backend for JavaScript consistency")
    
    return recommendations

def generate_integration_suggestions(context: Dict[str, Any]) -> List[str]:
    """Generate integration suggestions based on URL analysis."""
    suggestions = []
    
    tech_stack = context.get('tech_stack', [])
    business_model = context.get('business_model', '')
    
    if 'Stripe' in tech_stack:
        suggestions.append("Integrate with Stripe for payment processing")
    
    if business_model == 'ecommerce':
        suggestions.extend([
            "Consider inventory management system integration",
            "Add shipping provider APIs",
            "Integrate with email marketing platforms"
        ])
    elif business_model == 'saas':
        suggestions.extend([
            "Add authentication service integration",
            "Consider analytics platform integration",
            "Add customer support chat integration"
        ])
    
    return suggestions

def suggest_tech_stack(context: Dict[str, Any]) -> Dict[str, List[str]]:
    """Suggest tech stack based on URL analysis."""
    business_model = context.get('business_model', '')
    existing_tech = context.get('tech_stack', [])
    
    suggestions = {
        "frontend": [],
        "backend": [],
        "database": [],
        "integrations": []
    }
    
    # Frontend suggestions
    if 'React' in existing_tech:
        suggestions["frontend"] = ["React", "Next.js"]
    else:
        suggestions["frontend"] = ["React", "Vue.js"]
    
    # Backend suggestions
    if 'Node.js' in existing_tech:
        suggestions["backend"] = ["Node.js", "Express.js"]
    else:
        suggestions["backend"] = ["Node.js", "Python/FastAPI"]
    
    # Database suggestions
    if business_model == 'ecommerce':
        suggestions["database"] = ["PostgreSQL", "Redis"]
    elif business_model == 'social':
        suggestions["database"] = ["MongoDB", "Redis"]
    else:
        suggestions["database"] = ["PostgreSQL", "SQLite"]
    
    # Integration suggestions
    if business_model == 'ecommerce':
        suggestions["integrations"] = ["Stripe", "SendGrid"]
    elif business_model == 'saas':
        suggestions["integrations"] = ["Auth0", "Stripe"]
    else:
        suggestions["integrations"] = ["Auth0", "SendGrid"]
    
    return suggestions

def generate_url_insights(url_context: Dict[str, Any], features: List[EnhancedFeature]) -> Dict[str, Any]:
    """Generate insights based on URL context and project features."""
    insights = {
        "reference_system": {
            "title": url_context.get("title", "Unknown"),
            "business_model": url_context.get("business_model", "unknown"),
            "tech_stack": url_context.get("tech_stack", []),
            "key_features": url_context.get("extracted_features", [])
        },
        "compatibility_analysis": [],
        "feature_alignment": 0.0,
        "integration_opportunities": []
    }
    
    # Analyze feature alignment with reference system
    reference_features = url_context.get("extracted_features", [])
    project_features = [f.feature_name.lower() for f in features]
    
    aligned_features = 0
    for ref_feature in reference_features:
        for proj_feature in project_features:
            if any(word in ref_feature.lower() for word in proj_feature.split()):
                aligned_features += 1
                insights["compatibility_analysis"].append({
                    "project_feature": proj_feature,
                    "reference_feature": ref_feature,
                    "alignment": "high"
                })
                break
    
    # Calculate alignment score
    if reference_features and project_features:
        insights["feature_alignment"] = (aligned_features / len(project_features)) * 100
    
    # Integration opportunities
    tech_stack = url_context.get("tech_stack", [])
    if "Stripe" in tech_stack:
        insights["integration_opportunities"].append("Payment processing integration ready")
    if "React" in tech_stack:
        insights["integration_opportunities"].append("Frontend framework alignment available")
    
    return insights

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Ultimate MVP Generation Agent Server")
    print("📍 Server: http://localhost:8003")
    print("📖 API Docs: http://localhost:8003/docs")
    print("🎯 Features:")
    print("   • Tech Stack-Aware Effort Estimation")
    print("   • MVP Generation with Value Propositions")
    print("   • Enhanced URL Context Analysis")
    print("   • Dynamic MVP Re-evaluation")
    print("   • Comprehensive Project Analytics")
    print("=" * 60)
    
    uvicorn.run(
        "ultimate_mvp_server:app",
        host="0.0.0.0",
        port=8003,
        reload=False,
        log_level="info"
    )
