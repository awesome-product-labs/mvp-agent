"""
Enhanced models for MVP Generation Agent with tech stack awareness,
MVP definition, and value proposition generation.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl
from enum import Enum


class ValidationDecision(str, Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    DEFER = "DEFER"
    REJECT = "REJECT"


class ValidationScore(BaseModel):
    core_mvp_score: float
    complexity_score: float
    user_value_score: float
    overall_score: float


class ValidationResult(BaseModel):
    decision: ValidationDecision
    score: ValidationScore
    rationale: str
    alternatives: List[str]
    timeline_impact: str
    dependencies: List[str] = []
    confidence: float


class TechStack(str, Enum):
    # Frontend
    REACT = "React"
    VUE = "Vue.js"
    ANGULAR = "Angular"
    SVELTE = "Svelte"
    VANILLA_JS = "Vanilla JavaScript"
    
    # Backend
    NODEJS = "Node.js"
    PYTHON_DJANGO = "Python/Django"
    PYTHON_FASTAPI = "Python/FastAPI"
    RUBY_RAILS = "Ruby on Rails"
    DOTNET = "ASP.NET Core"
    PHP_LARAVEL = "PHP/Laravel"
    
    # Database
    POSTGRESQL = "PostgreSQL"
    MONGODB = "MongoDB"
    MYSQL = "MySQL"
    FIREBASE = "Firebase"
    SQLITE = "SQLite"
    
    # Cloud/Hosting
    AWS = "AWS"
    AZURE = "Azure"
    GCP = "Google Cloud"
    VERCEL = "Vercel"
    NETLIFY = "Netlify"
    HEROKU = "Heroku"
    
    # Integrations
    STRIPE = "Stripe"
    AUTH0 = "Auth0"
    SENDGRID = "SendGrid"
    TWILIO = "Twilio"


class TeamExperience(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class MVPStatus(str, Enum):
    UNDEFINED = "undefined"
    GENERATING = "generating"
    DEFINED = "defined"
    LOCKED = "locked"
    RE_EVALUATING = "re_evaluating"


class UserBenefit(BaseModel):
    user_type: str
    pain_point: str
    benefit: str
    value_metric: str
    feature_mapping: List[str]
    priority: str = "medium"  # high, medium, low


class CompetitiveAdvantage(BaseModel):
    advantage: str
    description: str
    supporting_features: List[str]
    market_gap: str


class ValueProposition(BaseModel):
    headline: str
    problem_statement: str
    solution_summary: str
    target_user_benefits: List[UserBenefit]
    competitive_advantages: List[CompetitiveAdvantage]
    success_metrics: List[str]
    user_journey_value: str
    market_positioning: str
    elevator_pitch: str
    generated_at: datetime
    confidence_score: float


class UserPersona(BaseModel):
    name: str
    description: str
    pain_points: List[str]
    goals: List[str]
    tech_savviness: str  # low, medium, high
    primary_benefits: List[str]


class CompetitiveAnalysis(BaseModel):
    direct_competitors: List[str]
    indirect_competitors: List[str]
    market_gaps: List[str]
    differentiation_opportunities: List[str]
    competitive_advantages: List[str]


class EffortEstimate(BaseModel):
    base_estimate_hours: float
    tech_stack_multiplier: float
    complexity_factor: float
    team_experience_factor: float
    integration_complexity: float
    final_estimate_hours: float
    final_estimate_weeks: float
    confidence_level: float
    breakdown: Dict[str, float]  # detailed breakdown by component


class MVPDefinition(BaseModel):
    id: str
    project_id: str
    core_features: List[str]  # Feature IDs
    rationale: str
    estimated_timeline_weeks: float
    estimated_effort_hours: float
    target_user_journey: str
    success_metrics: List[str]
    value_proposition: ValueProposition
    user_personas: List[UserPersona]
    competitive_analysis: CompetitiveAnalysis
    technical_requirements: List[str]
    assumptions: List[str]
    risks: List[str]
    defined_at: datetime
    status: MVPStatus = MVPStatus.DEFINED


class ProjectTechStack(BaseModel):
    frontend: List[TechStack] = []
    backend: List[TechStack] = []
    database: List[TechStack] = []
    cloud: List[TechStack] = []
    integrations: List[TechStack] = []
    custom_technologies: List[str] = []


class EnhancedProject(BaseModel):
    # Existing fields
    id: str
    name: str
    description: str
    industry: str
    target_users: str
    reference_url: Optional[HttpUrl] = None
    timeline_weeks: Optional[int] = None
    budget_range: Optional[str] = None
    team_size: Optional[int] = None
    status: str = "PLANNING"
    created_at: datetime
    updated_at: datetime
    total_features: int = 0
    approved_features: int = 0
    estimated_weeks: Optional[float] = None
    
    # Enhanced fields
    tech_stack: ProjectTechStack = ProjectTechStack()
    team_experience: TeamExperience = TeamExperience.INTERMEDIATE
    mvp_definition: Optional[MVPDefinition] = None
    mvp_status: MVPStatus = MVPStatus.UNDEFINED
    project_goals: List[str] = []
    target_market_size: Optional[str] = None
    business_model: Optional[str] = None


class EnhancedFeature(BaseModel):
    # Existing fields
    id: str
    project_id: str
    feature_name: str
    feature_description: str
    user_story: Optional[str] = None
    acceptance_criteria: List[str] = []
    priority: str = "medium"
    status: str = "PENDING"
    dependencies: List[str] = []
    estimated_weeks: Optional[float] = None
    validation_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    # Enhanced fields
    effort_estimate: Optional[EffortEstimate] = None
    technical_complexity: Optional[Dict[str, Any]] = None
    user_value_score: Optional[float] = None
    business_value_score: Optional[float] = None
    risk_factors: List[str] = []
    integration_requirements: List[str] = []


class MVPGenerationRequest(BaseModel):
    project_id: str
    include_pending_features: bool = False
    max_timeline_weeks: Optional[float] = None
    max_effort_hours: Optional[float] = None
    priority_threshold: Optional[str] = None  # only include features above this priority


class MVPValidationRequest(BaseModel):
    project_id: str
    feature_ids: List[str]
    validation_mode: str  # "validate_against_mvp" or "re_evaluate_mvp"


class MVPComparisonResult(BaseModel):
    current_mvp: Optional[MVPDefinition]
    proposed_mvp: MVPDefinition
    changes: Dict[str, Any]
    impact_analysis: Dict[str, Any]
    recommendations: List[str]


class ValuePropositionRequest(BaseModel):
    project_id: str
    mvp_definition_id: str
    target_audience_focus: Optional[str] = None
    competitive_context: Optional[Dict[str, Any]] = None


class TechStackEffortMultipliers(BaseModel):
    """Effort multipliers for different technology combinations"""
    frontend_multipliers: Dict[str, float] = {
        "React": 1.0,
        "Vue.js": 1.1,
        "Angular": 1.3,
        "Svelte": 1.2,
        "Vanilla JavaScript": 0.8
    }
    
    backend_multipliers: Dict[str, float] = {
        "Node.js": 1.0,
        "Python/Django": 1.1,
        "Python/FastAPI": 0.9,
        "Ruby on Rails": 1.2,
        "ASP.NET Core": 1.4,
        "PHP/Laravel": 1.1
    }
    
    database_multipliers: Dict[str, float] = {
        "PostgreSQL": 1.0,
        "MongoDB": 0.9,
        "MySQL": 1.0,
        "Firebase": 0.7,
        "SQLite": 0.6
    }
    
    integration_complexity: Dict[str, float] = {
        "Stripe": 0.8,  # Well documented, easy to integrate
        "Auth0": 0.7,   # Managed service, simple setup
        "SendGrid": 0.6,  # Simple email service
        "Twilio": 0.9   # More complex communication features
    }


class ProjectAnalyticsEnhanced(BaseModel):
    project_id: str
    total_features: int
    feature_breakdown: Dict[str, int]
    priority_breakdown: Dict[str, int]
    estimated_timeline: Optional[float] = None
    estimated_effort_hours: Optional[float] = None
    complexity_score: float
    mvp_readiness: float
    tech_stack_complexity: float
    team_velocity_estimate: float
    recommendations: List[str]
    risk_factors: List[str]
    suggested_phases: List[Dict[str, Any]]
    url_context_insights: Optional[Dict[str, Any]] = None
    mvp_insights: Optional[Dict[str, Any]] = None
    value_proposition_summary: Optional[str] = None
