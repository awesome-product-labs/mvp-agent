"""
Enhanced effort estimation service with tech stack awareness.
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..api.enhanced_models import (
    EffortEstimate, ProjectTechStack, TeamExperience, TechStackEffortMultipliers,
    EnhancedFeature, EnhancedProject
)

logger = logging.getLogger(__name__)


class EffortEstimationService:
    """Service for calculating tech stack-aware effort estimates."""
    
    def __init__(self):
        self.multipliers = TechStackEffortMultipliers()
        
        # Base effort estimates for common feature types (in hours)
        self.base_estimates = {
            # Authentication & User Management
            "authentication": 40,
            "user registration": 24,
            "user profile": 32,
            "password reset": 16,
            "social login": 20,
            
            # Core CRUD Operations
            "basic crud": 32,
            "advanced crud": 48,
            "data import/export": 40,
            "search functionality": 36,
            "filtering": 24,
            
            # UI/UX Components
            "dashboard": 60,
            "forms": 20,
            "navigation": 16,
            "responsive design": 32,
            "mobile optimization": 40,
            
            # E-commerce
            "shopping cart": 48,
            "checkout process": 72,
            "payment integration": 56,
            "inventory management": 64,
            "order tracking": 40,
            
            # Communication
            "messaging system": 80,
            "notifications": 32,
            "email integration": 24,
            "real-time chat": 96,
            
            # Analytics & Reporting
            "basic analytics": 48,
            "advanced reporting": 80,
            "data visualization": 56,
            "export reports": 32,
            
            # Integration & APIs
            "third-party api": 40,
            "webhook integration": 32,
            "api development": 48,
            "data synchronization": 56,
            
            # Advanced Features
            "machine learning": 160,
            "ai integration": 120,
            "recommendation engine": 200,
            "advanced search": 80,
            "real-time features": 96,
            
            # Security & Compliance
            "security features": 48,
            "data encryption": 40,
            "compliance features": 64,
            "audit logging": 32,
            
            # Default fallback
            "default": 40
        }
        
        # Team experience multipliers
        self.experience_multipliers = {
            TeamExperience.BEGINNER: 1.8,
            TeamExperience.INTERMEDIATE: 1.0,
            TeamExperience.ADVANCED: 0.7,
            TeamExperience.EXPERT: 0.5
        }
        
        # Complexity multipliers based on feature description keywords
        self.complexity_keywords = {
            "simple": 0.7,
            "basic": 0.8,
            "standard": 1.0,
            "advanced": 1.4,
            "complex": 1.8,
            "enterprise": 2.0,
            "real-time": 1.6,
            "machine learning": 2.5,
            "ai": 2.2,
            "integration": 1.3,
            "custom": 1.5,
            "scalable": 1.4,
            "secure": 1.2,
            "compliant": 1.3
        }
    
    def estimate_feature_effort(
        self,
        feature: EnhancedFeature,
        project: EnhancedProject,
        context: Optional[Dict[str, Any]] = None
    ) -> EffortEstimate:
        """Calculate comprehensive effort estimate for a feature."""
        
        # Get base estimate
        base_hours = self._get_base_estimate(feature)
        
        # Calculate multipliers
        tech_multiplier = self._calculate_tech_stack_multiplier(feature, project.tech_stack)
        complexity_factor = self._calculate_complexity_factor(feature)
        experience_factor = self.experience_multipliers.get(project.team_experience, 1.0)
        integration_complexity = self._calculate_integration_complexity(feature, project.tech_stack)
        
        # Calculate final estimate
        final_hours = (
            base_hours * 
            tech_multiplier * 
            complexity_factor * 
            experience_factor * 
            integration_complexity
        )
        
        final_weeks = final_hours / 40  # Assuming 40 hours per week
        
        # Calculate confidence based on various factors
        confidence = self._calculate_confidence(feature, project, context)
        
        # Create detailed breakdown
        breakdown = {
            "base_estimate": base_hours,
            "tech_stack_impact": base_hours * (tech_multiplier - 1),
            "complexity_impact": base_hours * tech_multiplier * (complexity_factor - 1),
            "experience_impact": base_hours * tech_multiplier * complexity_factor * (experience_factor - 1),
            "integration_impact": base_hours * tech_multiplier * complexity_factor * experience_factor * (integration_complexity - 1)
        }
        
        return EffortEstimate(
            base_estimate_hours=base_hours,
            tech_stack_multiplier=tech_multiplier,
            complexity_factor=complexity_factor,
            team_experience_factor=experience_factor,
            integration_complexity=integration_complexity,
            final_estimate_hours=round(final_hours, 1),
            final_estimate_weeks=round(final_weeks, 1),
            confidence_level=confidence,
            breakdown=breakdown
        )
    
    def _get_base_estimate(self, feature: EnhancedFeature) -> float:
        """Get base effort estimate based on feature type."""
        feature_name = feature.feature_name.lower()
        feature_desc = feature.feature_description.lower()
        
        # Try to match feature type based on name and description
        for feature_type, hours in self.base_estimates.items():
            if feature_type in feature_name or feature_type in feature_desc:
                return hours
        
        # Fallback: estimate based on description length and complexity
        desc_length = len(feature.feature_description)
        if desc_length < 50:
            return 24  # Simple feature
        elif desc_length < 150:
            return 40  # Medium feature
        else:
            return 64  # Complex feature
    
    def _calculate_tech_stack_multiplier(
        self, 
        feature: EnhancedFeature, 
        tech_stack: ProjectTechStack
    ) -> float:
        """Calculate tech stack complexity multiplier."""
        multiplier = 1.0
        
        # Frontend multiplier
        if tech_stack.frontend:
            frontend_tech = tech_stack.frontend[0].value  # Use primary frontend tech
            multiplier *= self.multipliers.frontend_multipliers.get(frontend_tech, 1.0)
        
        # Backend multiplier
        if tech_stack.backend:
            backend_tech = tech_stack.backend[0].value  # Use primary backend tech
            multiplier *= self.multipliers.backend_multipliers.get(backend_tech, 1.0)
        
        # Database multiplier
        if tech_stack.database:
            db_tech = tech_stack.database[0].value  # Use primary database
            multiplier *= self.multipliers.database_multipliers.get(db_tech, 1.0)
        
        # Multiple technologies penalty (complexity increases with more tech)
        total_technologies = (
            len(tech_stack.frontend) + 
            len(tech_stack.backend) + 
            len(tech_stack.database) + 
            len(tech_stack.cloud) + 
            len(tech_stack.integrations)
        )
        
        if total_technologies > 5:
            multiplier *= 1.2  # 20% penalty for complex tech stack
        elif total_technologies > 8:
            multiplier *= 1.4  # 40% penalty for very complex tech stack
        
        return multiplier
    
    def _calculate_complexity_factor(self, feature: EnhancedFeature) -> float:
        """Calculate complexity factor based on feature description."""
        description = feature.feature_description.lower()
        factor = 1.0
        
        # Check for complexity keywords
        for keyword, multiplier in self.complexity_keywords.items():
            if keyword in description:
                factor *= multiplier
                break  # Use first match to avoid compounding
        
        # Additional complexity factors
        if len(feature.acceptance_criteria) > 5:
            factor *= 1.2  # Many acceptance criteria = more complex
        
        if len(feature.dependencies) > 2:
            factor *= 1.3  # Many dependencies = more complex
        
        # Cap the complexity factor to reasonable bounds
        return min(factor, 3.0)
    
    def _calculate_integration_complexity(
        self, 
        feature: EnhancedFeature, 
        tech_stack: ProjectTechStack
    ) -> float:
        """Calculate integration complexity multiplier."""
        complexity = 1.0
        
        # Integration services complexity
        for integration in tech_stack.integrations:
            integration_multiplier = self.multipliers.integration_complexity.get(
                integration.value, 1.0
            )
            complexity *= integration_multiplier
        
        # Feature-specific integration complexity
        feature_desc = feature.feature_description.lower()
        
        if "payment" in feature_desc or "stripe" in feature_desc:
            complexity *= 0.9  # Payment integrations are well-documented
        elif "auth" in feature_desc and "auth0" in str(tech_stack.integrations):
            complexity *= 0.8  # Auth0 makes auth easier
        elif "email" in feature_desc:
            complexity *= 0.7  # Email services are straightforward
        elif "api" in feature_desc and "integration" in feature_desc:
            complexity *= 1.4  # Custom API integrations are more complex
        
        return complexity
    
    def _calculate_confidence(
        self, 
        feature: EnhancedFeature, 
        project: EnhancedProject,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """Calculate confidence level for the estimate."""
        confidence = 0.8  # Base confidence
        
        # Higher confidence for well-defined features
        if feature.acceptance_criteria and len(feature.acceptance_criteria) > 2:
            confidence += 0.1
        
        if feature.user_story:
            confidence += 0.05
        
        # Higher confidence for experienced teams
        if project.team_experience == TeamExperience.ADVANCED:
            confidence += 0.1
        elif project.team_experience == TeamExperience.EXPERT:
            confidence += 0.15
        elif project.team_experience == TeamExperience.BEGINNER:
            confidence -= 0.2
        
        # Lower confidence for very complex features
        if "machine learning" in feature.feature_description.lower():
            confidence -= 0.2
        elif "ai" in feature.feature_description.lower():
            confidence -= 0.15
        
        # Higher confidence for common tech stacks
        if any("React" in str(tech) for tech in project.tech_stack.frontend):
            confidence += 0.05
        if any("Node.js" in str(tech) for tech in project.tech_stack.backend):
            confidence += 0.05
        
        # Context-based adjustments
        if context:
            # If similar features exist in reference URL, higher confidence
            if context.get('url_context') and context['url_context'].get('extracted_features'):
                similar_features = [
                    f for f in context['url_context']['extracted_features']
                    if any(word in f.lower() for word in feature.feature_name.lower().split())
                ]
                if similar_features:
                    confidence += 0.1
        
        return min(max(confidence, 0.3), 0.95)  # Clamp between 30% and 95%
    
    def estimate_project_effort(
        self, 
        features: List[EnhancedFeature], 
        project: EnhancedProject
    ) -> Dict[str, Any]:
        """Calculate total project effort estimate."""
        
        total_hours = 0
        total_weeks = 0
        feature_estimates = []
        
        for feature in features:
            if feature.status in ["APPROVED", "IN_DEVELOPMENT"]:
                estimate = self.estimate_feature_effort(feature, project)
                feature_estimates.append({
                    "feature_id": feature.id,
                    "feature_name": feature.feature_name,
                    "estimate": estimate
                })
                total_hours += estimate.final_estimate_hours
                total_weeks += estimate.final_estimate_weeks
        
        # Project overhead (testing, deployment, project management)
        overhead_multiplier = 1.3
        total_hours_with_overhead = total_hours * overhead_multiplier
        total_weeks_with_overhead = total_weeks * overhead_multiplier
        
        # Team velocity adjustment
        team_velocity = self._calculate_team_velocity(project)
        adjusted_weeks = total_weeks_with_overhead / team_velocity
        
        return {
            "total_features": len(features),
            "estimated_features": len(feature_estimates),
            "total_effort_hours": round(total_hours, 1),
            "total_effort_weeks": round(total_weeks, 1),
            "total_with_overhead_hours": round(total_hours_with_overhead, 1),
            "total_with_overhead_weeks": round(total_weeks_with_overhead, 1),
            "team_velocity_adjusted_weeks": round(adjusted_weeks, 1),
            "team_velocity_factor": team_velocity,
            "overhead_factor": overhead_multiplier,
            "feature_estimates": feature_estimates
        }
    
    def _calculate_team_velocity(self, project: EnhancedProject) -> float:
        """Calculate team velocity multiplier based on team size and experience."""
        base_velocity = 1.0
        
        # Team size impact
        if project.team_size:
            if project.team_size == 1:
                base_velocity = 0.8  # Solo developer penalty
            elif project.team_size <= 3:
                base_velocity = 1.0  # Optimal small team
            elif project.team_size <= 6:
                base_velocity = 1.2  # Good medium team
            else:
                base_velocity = 0.9  # Large team coordination overhead
        
        # Experience impact on velocity
        experience_velocity = {
            TeamExperience.BEGINNER: 0.6,
            TeamExperience.INTERMEDIATE: 1.0,
            TeamExperience.ADVANCED: 1.3,
            TeamExperience.EXPERT: 1.5
        }
        
        return base_velocity * experience_velocity.get(project.team_experience, 1.0)
