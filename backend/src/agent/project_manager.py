"""
Project management service for handling multi-feature MVP projects.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

from ..api.project_models import (
    Project, ProjectCreate, ProjectFeature, ProjectAnalysis,
    URLContext, FeatureStatus, ProjectStatus, FeatureInteraction,
    ProjectPhase, ProjectRoadmap
)
from ..api.models import FeatureRequest, ValidationResult
from ..utils.url_analyzer import URLAnalyzer
from .validators import MVPFeatureValidator

logger = logging.getLogger(__name__)


class ProjectManager:
    """Service for managing MVP projects with multiple features."""
    
    def __init__(self, validator: MVPFeatureValidator, url_analyzer: URLAnalyzer):
        self.validator = validator
        self.url_analyzer = url_analyzer
        
        # In-memory storage (in production, use a database)
        self.projects: Dict[str, Project] = {}
        self.project_features: Dict[str, List[ProjectFeature]] = defaultdict(list)
        self.url_contexts: Dict[str, URLContext] = {}
        
    async def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a new MVP project."""
        project_id = str(uuid.uuid4())
        
        # Analyze reference URL if provided
        url_context = None
        if project_data.reference_url:
            try:
                url_context = await self.url_analyzer.analyze_url(project_data.reference_url)
                self.url_contexts[project_id] = url_context
                logger.info(f"URL analysis completed for project {project_id}")
            except Exception as e:
                logger.error(f"URL analysis failed for {project_data.reference_url}: {str(e)}")
        
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
        
        self.projects[project_id] = project
        logger.info(f"Created project: {project.name} (ID: {project_id})")
        
        return project
    
    async def add_feature_to_project(self, project_id: str, feature_request: FeatureRequest) -> ProjectFeature:
        """Add a feature to a project and validate it with project context."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        # Enhanced validation with project context
        validation_context = self._build_validation_context(project_id)
        enhanced_request = self._enhance_feature_request(feature_request, validation_context)
        
        # Validate the feature
        validation_result = await self.validator.validate_feature(enhanced_request)
        
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
            status=self._determine_feature_status(validation_result),
            dependencies=[],
            estimated_weeks=self._estimate_feature_timeline(validation_result),
            validation_result=validation_result.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Add to project
        self.project_features[project_id].append(project_feature)
        
        # Update project stats
        await self._update_project_stats(project_id)
        
        logger.info(f"Added feature '{feature_request.name}' to project {project_id}")
        return project_feature
    
    async def analyze_project(self, project_id: str) -> ProjectAnalysis:
        """Perform comprehensive project analysis."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        features = self.project_features[project_id]
        url_context = self.url_contexts.get(project_id)
        
        # Feature breakdown by status
        feature_breakdown = defaultdict(int)
        for feature in features:
            feature_breakdown[feature.status.value] += 1
        
        # Priority breakdown
        priority_breakdown = defaultdict(int)
        for feature in features:
            priority_breakdown[feature.priority] += 1
        
        # Calculate metrics
        total_features = len(features)
        complexity_score = self._calculate_project_complexity(features)
        mvp_readiness = self._calculate_mvp_readiness(features)
        estimated_timeline = self._calculate_project_timeline(features)
        
        # Generate recommendations
        recommendations = self._generate_project_recommendations(project, features, url_context)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(project, features)
        
        # Suggest development phases
        suggested_phases = self._suggest_development_phases(features)
        
        # URL context insights
        url_context_insights = None
        if url_context:
            url_context_insights = self._generate_url_insights(url_context, features)
        
        analysis = ProjectAnalysis(
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
        
        return analysis
    
    def _build_validation_context(self, project_id: str) -> Dict[str, Any]:
        """Build context for enhanced feature validation."""
        project = self.projects[project_id]
        existing_features = self.project_features[project_id]
        url_context = self.url_contexts.get(project_id)
        
        context = {
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
        
        return context
    
    def _enhance_feature_request(self, feature_request: FeatureRequest, context: Dict[str, Any]) -> FeatureRequest:
        """Enhance feature request with project context."""
        enhanced_request = feature_request.copy()
        enhanced_request.context = context
        return enhanced_request
    
    def _determine_feature_status(self, validation_result: ValidationResult) -> FeatureStatus:
        """Determine feature status based on validation result."""
        if validation_result.decision.value == "ACCEPT":
            return FeatureStatus.APPROVED
        elif validation_result.decision.value == "REJECT":
            return FeatureStatus.REJECTED
        else:
            return FeatureStatus.PENDING
    
    def _estimate_feature_timeline(self, validation_result: ValidationResult) -> Optional[float]:
        """Estimate feature development timeline."""
        complexity = validation_result.score.complexity_score
        
        # Simple timeline estimation based on complexity
        if complexity <= 3:
            return 1.0  # 1 week
        elif complexity <= 5:
            return 2.0  # 2 weeks
        elif complexity <= 7:
            return 4.0  # 4 weeks
        else:
            return 8.0  # 8+ weeks
    
    async def _update_project_stats(self, project_id: str):
        """Update project statistics."""
        project = self.projects[project_id]
        features = self.project_features[project_id]
        
        project.total_features = len(features)
        project.approved_features = sum(1 for f in features if f.status == FeatureStatus.APPROVED)
        project.estimated_weeks = sum(f.estimated_weeks or 0 for f in features)
        project.updated_at = datetime.now()
    
    def _calculate_project_complexity(self, features: List[ProjectFeature]) -> float:
        """Calculate overall project complexity score."""
        if not features:
            return 0.0
        
        total_complexity = 0.0
        for feature in features:
            if feature.validation_result:
                complexity = feature.validation_result.get('score', {}).get('complexity_score', 5.0)
                total_complexity += complexity
        
        return total_complexity / len(features)
    
    def _calculate_mvp_readiness(self, features: List[ProjectFeature]) -> float:
        """Calculate MVP readiness score."""
        if not features:
            return 0.0
        
        approved_features = [f for f in features if f.status == FeatureStatus.APPROVED]
        high_priority_features = [f for f in features if f.priority == "high"]
        
        # MVP readiness based on approved features and priorities
        approval_ratio = len(approved_features) / len(features)
        priority_coverage = len([f for f in approved_features if f.priority == "high"]) / max(len(high_priority_features), 1)
        
        return (approval_ratio * 0.6 + priority_coverage * 0.4) * 10
    
    def _calculate_project_timeline(self, features: List[ProjectFeature]) -> Optional[float]:
        """Calculate estimated project timeline."""
        approved_features = [f for f in features if f.status == FeatureStatus.APPROVED]
        
        if not approved_features:
            return None
        
        return sum(f.estimated_weeks or 0 for f in approved_features)
    
    def _generate_project_recommendations(self, project: Project, features: List[ProjectFeature], url_context: Optional[URLContext]) -> List[str]:
        """Generate project-specific recommendations."""
        recommendations = []
        
        # Feature-based recommendations
        approved_count = sum(1 for f in features if f.status == FeatureStatus.APPROVED)
        pending_count = sum(1 for f in features if f.status == FeatureStatus.PENDING)
        
        if approved_count < 3:
            recommendations.append("Consider adding more core features to create a viable MVP")
        
        if pending_count > approved_count:
            recommendations.append("Review and refine pending features to improve approval rate")
        
        # Timeline recommendations
        if project.estimated_weeks and project.estimated_weeks > 26:  # 6 months
            recommendations.append("Consider breaking the project into smaller phases")
        
        # URL context recommendations
        if url_context:
            if url_context.business_model == "ecommerce" and project.industry.value != "E-COMMERCE":
                recommendations.append("Consider aligning with the e-commerce nature of the reference system")
        
        return recommendations
    
    def _identify_risk_factors(self, project: Project, features: List[ProjectFeature]) -> List[str]:
        """Identify project risk factors."""
        risks = []
        
        # Complexity risks
        high_complexity_features = [
            f for f in features 
            if f.validation_result and f.validation_result.get('score', {}).get('complexity_score', 0) > 7
        ]
        
        if len(high_complexity_features) > len(features) * 0.3:
            risks.append("High number of complex features may impact timeline")
        
        # Timeline risks
        if project.timeline_weeks and project.estimated_weeks:
            if project.estimated_weeks > project.timeline_weeks:
                risks.append("Estimated timeline exceeds project deadline")
        
        # Team size risks
        if project.team_size and project.team_size < 3 and len(features) > 10:
            risks.append("Small team size may struggle with large feature set")
        
        return risks
    
    def _suggest_development_phases(self, features: List[ProjectFeature]) -> List[Dict[str, Any]]:
        """Suggest development phases based on features."""
        phases = []
        
        # Phase 1: Core features (high priority, approved)
        core_features = [
            f for f in features 
            if f.status == FeatureStatus.APPROVED and f.priority == "high"
        ]
        
        if core_features:
            phases.append({
                "phase": 1,
                "name": "Core MVP",
                "features": [f.feature_name for f in core_features],
                "estimated_weeks": sum(f.estimated_weeks or 0 for f in core_features),
                "description": "Essential features for initial launch"
            })
        
        # Phase 2: Enhancement features (medium priority, approved)
        enhancement_features = [
            f for f in features 
            if f.status == FeatureStatus.APPROVED and f.priority == "medium"
        ]
        
        if enhancement_features:
            phases.append({
                "phase": 2,
                "name": "Feature Enhancement",
                "features": [f.feature_name for f in enhancement_features],
                "estimated_weeks": sum(f.estimated_weeks or 0 for f in enhancement_features),
                "description": "Additional features to improve user experience"
            })
        
        return phases
    
    def _generate_url_insights(self, url_context: URLContext, features: List[ProjectFeature]) -> Dict[str, Any]:
        """Generate insights based on URL context analysis."""
        insights = {
            "reference_system": {
                "title": url_context.title,
                "business_model": url_context.business_model,
                "tech_stack": url_context.tech_stack,
                "key_features": url_context.extracted_features
            },
            "compatibility_analysis": [],
            "integration_opportunities": [],
            "potential_conflicts": []
        }
        
        # Analyze feature compatibility with reference system
        for feature in features:
            if feature.status == FeatureStatus.APPROVED:
                # Check if feature aligns with reference system
                feature_lower = feature.feature_name.lower()
                
                # Look for similar features in reference system
                similar_features = [
                    ref_feature for ref_feature in url_context.extracted_features
                    if any(word in ref_feature.lower() for word in feature_lower.split())
                ]
                
                if similar_features:
                    insights["compatibility_analysis"].append({
                        "feature": feature.feature_name,
                        "similar_in_reference": similar_features,
                        "recommendation": "Consider how this feature will integrate with existing functionality"
                    })
        
        return insights
