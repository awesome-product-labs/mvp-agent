"""
Extended data models for project management and URL context analysis.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, HttpUrl, Field


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


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    industry: Industry
    target_users: str = Field(..., min_length=5, max_length=500)
    reference_url: Optional[HttpUrl] = None
    timeline_weeks: Optional[int] = Field(None, ge=1, le=104)  # 1-104 weeks (2 years)
    budget_range: Optional[str] = None
    team_size: Optional[int] = Field(None, ge=1, le=50)


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


class ProjectAnalysis(BaseModel):
    project_id: str
    total_features: int
    feature_breakdown: Dict[str, int]  # status -> count
    priority_breakdown: Dict[str, int]  # priority -> count
    estimated_timeline: Optional[float] = None
    complexity_score: float
    mvp_readiness: float
    recommendations: List[str]
    risk_factors: List[str]
    suggested_phases: List[Dict[str, Any]]
    url_context_insights: Optional[Dict[str, Any]] = None


class BatchFeatureRequest(BaseModel):
    project_id: str
    features: List[Dict[str, Any]]  # List of feature data


class ProjectFeatureResponse(BaseModel):
    project: Project
    features: List[ProjectFeature]
    analysis: ProjectAnalysis
    url_context: Optional[URLContext] = None


class FeatureDependency(BaseModel):
    feature_id: str
    depends_on: str
    dependency_type: str = "blocks"  # blocks, enhances, conflicts
    description: Optional[str] = None


class ProjectPhase(BaseModel):
    phase_number: int
    name: str
    description: str
    features: List[str]  # feature IDs
    estimated_weeks: float
    dependencies: List[str] = []
    deliverables: List[str] = []


class ProjectRoadmap(BaseModel):
    project_id: str
    phases: List[ProjectPhase]
    total_timeline: float
    critical_path: List[str]
    risk_mitigation: List[str]
    success_metrics: List[str]


class URLAnalysisRequest(BaseModel):
    url: HttpUrl
    analysis_depth: str = "standard"  # basic, standard, deep


class URLAnalysisResponse(BaseModel):
    url: HttpUrl
    context: URLContext
    recommendations: List[str]
    competitive_insights: List[str]
    integration_suggestions: List[str]


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    timeline_weeks: Optional[int] = None
    budget_range: Optional[str] = None
    team_size: Optional[int] = None


class FeatureInteraction(BaseModel):
    feature1_id: str
    feature2_id: str
    interaction_type: str  # synergy, conflict, dependency, redundancy
    impact_score: float  # -1 to 1, negative for conflicts
    description: str
    recommendation: str


class ProjectMetrics(BaseModel):
    project_id: str
    completion_percentage: float
    features_completed: int
    features_in_progress: int
    features_pending: int
    average_feature_complexity: float
    timeline_adherence: float  # percentage
    budget_utilization: Optional[float] = None
    team_velocity: Optional[float] = None  # features per week
    quality_score: Optional[float] = None
