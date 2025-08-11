"""
MVP Generation Service with AI-powered value proposition generation.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from ..api.enhanced_models import (
    MVPDefinition, ValueProposition, UserBenefit, CompetitiveAdvantage,
    UserPersona, CompetitiveAnalysis, EnhancedProject, EnhancedFeature,
    MVPStatus, MVPGenerationRequest, MVPValidationRequest, MVPComparisonResult
)
from .effort_estimation import EffortEstimationService

logger = logging.getLogger(__name__)


class MVPGeneratorService:
    """Service for generating MVP definitions and value propositions."""
    
    def __init__(self, effort_service: EffortEstimationService):
        self.effort_service = effort_service
        
        # Value proposition templates by industry
        self.industry_templates = {
            "E-COMMERCE": {
                "problem_keywords": ["shopping", "buying", "selling", "inventory", "payment", "checkout"],
                "value_themes": ["convenience", "security", "speed", "selection", "price"],
                "success_metrics": ["conversion rate", "average order value", "customer acquisition cost", "time to purchase"]
            },
            "FINTECH": {
                "problem_keywords": ["money", "payment", "banking", "investment", "financial", "transaction"],
                "value_themes": ["security", "transparency", "accessibility", "efficiency", "compliance"],
                "success_metrics": ["transaction volume", "user adoption", "security incidents", "regulatory compliance"]
            },
            "HEALTHCARE": {
                "problem_keywords": ["health", "medical", "patient", "doctor", "treatment", "diagnosis"],
                "value_themes": ["accessibility", "accuracy", "privacy", "efficiency", "outcomes"],
                "success_metrics": ["patient outcomes", "time to diagnosis", "cost reduction", "user satisfaction"]
            },
            "EDUCATION": {
                "problem_keywords": ["learning", "teaching", "student", "course", "knowledge", "skill"],
                "value_themes": ["accessibility", "engagement", "personalization", "effectiveness", "affordability"],
                "success_metrics": ["learning outcomes", "engagement rate", "completion rate", "knowledge retention"]
            },
            "SOCIAL": {
                "problem_keywords": ["connect", "share", "community", "communication", "social", "network"],
                "value_themes": ["connection", "engagement", "privacy", "authenticity", "discovery"],
                "success_metrics": ["daily active users", "engagement rate", "content creation", "user retention"]
            },
            "PRODUCTIVITY": {
                "problem_keywords": ["work", "task", "project", "team", "collaboration", "efficiency"],
                "value_themes": ["efficiency", "collaboration", "organization", "automation", "integration"],
                "success_metrics": ["time saved", "task completion rate", "team productivity", "user adoption"]
            }
        }
    
    async def generate_mvp(
        self, 
        request: MVPGenerationRequest,
        project: EnhancedProject,
        features: List[EnhancedFeature],
        url_context: Optional[Dict[str, Any]] = None
    ) -> MVPDefinition:
        """Generate comprehensive MVP definition with value proposition."""
        
        logger.info(f"Generating MVP for project {request.project_id}")
        
        # Filter and prioritize features for MVP
        mvp_features = self._select_mvp_features(
            features, request.max_timeline_weeks, request.max_effort_hours, request.priority_threshold
        )
        
        # Calculate effort estimates
        effort_estimate = self.effort_service.estimate_project_effort(mvp_features, project)
        
        # Generate core MVP components
        rationale = self._generate_mvp_rationale(mvp_features, project, url_context)
        user_journey = self._generate_user_journey(mvp_features, project)
        success_metrics = self._generate_success_metrics(project, mvp_features)
        technical_requirements = self._generate_technical_requirements(mvp_features, project)
        assumptions = self._generate_assumptions(project, mvp_features, url_context)
        risks = self._identify_risks(project, mvp_features)
        
        # Generate user personas
        user_personas = self._generate_user_personas(project, mvp_features, url_context)
        
        # Generate competitive analysis
        competitive_analysis = self._generate_competitive_analysis(project, url_context)
        
        # Generate value proposition
        value_proposition = self._generate_value_proposition(
            project, mvp_features, user_personas, competitive_analysis, url_context
        )
        
        # Create MVP definition
        mvp_definition = MVPDefinition(
            id=str(uuid.uuid4()),
            project_id=request.project_id,
            core_features=[f.id for f in mvp_features],
            rationale=rationale,
            estimated_timeline_weeks=effort_estimate["team_velocity_adjusted_weeks"],
            estimated_effort_hours=effort_estimate["total_with_overhead_hours"],
            target_user_journey=user_journey,
            success_metrics=success_metrics,
            value_proposition=value_proposition,
            user_personas=user_personas,
            competitive_analysis=competitive_analysis,
            technical_requirements=technical_requirements,
            assumptions=assumptions,
            risks=risks,
            defined_at=datetime.now(),
            status=MVPStatus.DEFINED
        )
        
        logger.info(f"MVP generated with {len(mvp_features)} features, {effort_estimate['team_velocity_adjusted_weeks']:.1f} weeks timeline")
        
        return mvp_definition
    
    def _select_mvp_features(
        self, 
        features: List[EnhancedFeature],
        max_timeline_weeks: Optional[float] = None,
        max_effort_hours: Optional[float] = None,
        priority_threshold: Optional[str] = None
    ) -> List[EnhancedFeature]:
        """Select optimal features for MVP based on constraints."""
        
        # Filter by status (only approved features)
        approved_features = [f for f in features if f.status == "APPROVED"]
        
        # Filter by priority if specified
        if priority_threshold:
            priority_order = {"high": 3, "medium": 2, "low": 1}
            threshold_value = priority_order.get(priority_threshold, 0)
            approved_features = [
                f for f in approved_features 
                if priority_order.get(f.priority, 0) >= threshold_value
            ]
        
        # Sort by priority and value
        def feature_score(feature):
            priority_score = {"high": 3, "medium": 2, "low": 1}.get(feature.priority, 1)
            # Add validation score if available
            validation_score = 0
            if feature.validation_result and 'score' in feature.validation_result:
                validation_score = feature.validation_result['score'].get('overall_score', 0)
            return priority_score * 10 + validation_score
        
        approved_features.sort(key=feature_score, reverse=True)
        
        # Apply constraints
        selected_features = []
        total_weeks = 0
        total_hours = 0
        
        for feature in approved_features:
            feature_weeks = feature.estimated_weeks or 2.0
            feature_hours = feature_weeks * 40
            
            # Check constraints
            if max_timeline_weeks and (total_weeks + feature_weeks) > max_timeline_weeks:
                continue
            if max_effort_hours and (total_hours + feature_hours) > max_effort_hours:
                continue
            
            selected_features.append(feature)
            total_weeks += feature_weeks
            total_hours += feature_hours
        
        # Ensure minimum viable set (at least 3 core features)
        if len(selected_features) < 3 and len(approved_features) >= 3:
            selected_features = approved_features[:3]
        
        return selected_features
    
    def _generate_mvp_rationale(
        self, 
        features: List[EnhancedFeature], 
        project: EnhancedProject,
        url_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate rationale for MVP feature selection."""
        
        feature_names = [f.feature_name for f in features]
        high_priority_count = sum(1 for f in features if f.priority == "high")
        
        rationale = f"This MVP focuses on {len(features)} core features that deliver maximum user value with minimal complexity. "
        
        if high_priority_count > 0:
            rationale += f"It includes {high_priority_count} high-priority features that are essential for the target user journey. "
        
        # Add industry-specific rationale
        if project.industry in self.industry_templates:
            template = self.industry_templates[project.industry]
            rationale += f"For the {project.industry.lower()} industry, this MVP addresses key user needs around {', '.join(template['value_themes'][:3])}. "
        
        # Add competitive context if available
        if url_context and url_context.get('business_model'):
            rationale += f"Based on analysis of similar {url_context['business_model']} solutions, this feature set provides a competitive foundation while remaining achievable for an MVP. "
        
        rationale += f"The selected features ({', '.join(feature_names)}) create a cohesive user experience that validates the core value proposition."
        
        return rationale
    
    def _generate_user_journey(self, features: List[EnhancedFeature], project: EnhancedProject) -> str:
        """Generate target user journey description."""
        
        # Analyze features to construct logical user flow
        auth_features = [f for f in features if "auth" in f.feature_name.lower() or "login" in f.feature_name.lower()]
        core_features = [f for f in features if f not in auth_features]
        
        journey = f"Target users ({project.target_users}) will: "
        
        if auth_features:
            journey += "1) Register/login to access the platform, "
        
        # Add core functionality steps
        for i, feature in enumerate(core_features[:3], start=2 if auth_features else 1):
            action = self._feature_to_user_action(feature)
            journey += f"{i}) {action}, "
        
        journey += f"ultimately achieving their goal of {self._infer_user_goal(project, features)}."
        
        return journey
    
    def _feature_to_user_action(self, feature: EnhancedFeature) -> str:
        """Convert feature to user action description."""
        name = feature.feature_name.lower()
        
        if "dashboard" in name:
            return "view their personalized dashboard"
        elif "search" in name:
            return "search and discover relevant content"
        elif "create" in name or "add" in name:
            return "create and manage their content"
        elif "profile" in name:
            return "set up and customize their profile"
        elif "payment" in name or "checkout" in name:
            return "complete secure transactions"
        elif "message" in name or "chat" in name:
            return "communicate with other users"
        else:
            return f"use {feature.feature_name.lower()}"
    
    def _infer_user_goal(self, project: EnhancedProject, features: List[EnhancedFeature]) -> str:
        """Infer primary user goal from project and features."""
        industry = project.industry.lower()
        
        if "ecommerce" in industry or "e-commerce" in industry:
            return "making purchases efficiently and securely"
        elif "social" in industry:
            return "connecting and engaging with their community"
        elif "productivity" in industry:
            return "improving their work efficiency and collaboration"
        elif "education" in industry:
            return "learning new skills and knowledge effectively"
        elif "healthcare" in industry:
            return "managing their health and wellness"
        elif "fintech" in industry:
            return "managing their finances securely and efficiently"
        else:
            return "solving their core problem efficiently"
    
    def _generate_success_metrics(self, project: EnhancedProject, features: List[EnhancedFeature]) -> List[str]:
        """Generate relevant success metrics for the MVP."""
        
        metrics = []
        
        # Industry-specific metrics
        if project.industry in self.industry_templates:
            template = self.industry_templates[project.industry]
            metrics.extend(template["success_metrics"][:3])
        
        # Feature-specific metrics
        feature_names = " ".join([f.feature_name.lower() for f in features])
        
        if "auth" in feature_names or "login" in feature_names:
            metrics.append("user registration rate")
        
        if "dashboard" in feature_names:
            metrics.append("daily active users")
        
        if "search" in feature_names:
            metrics.append("search success rate")
        
        if "payment" in feature_names or "checkout" in feature_names:
            metrics.append("transaction completion rate")
        
        # Generic MVP metrics
        metrics.extend([
            "user retention rate (30-day)",
            "feature adoption rate",
            "user satisfaction score",
            "time to value (first meaningful action)"
        ])
        
        # Remove duplicates and limit to top 6
        return list(dict.fromkeys(metrics))[:6]
    
    def _generate_technical_requirements(self, features: List[EnhancedFeature], project: EnhancedProject) -> List[str]:
        """Generate technical requirements based on features and tech stack."""
        
        requirements = []
        
        # Tech stack requirements
        if project.tech_stack.frontend:
            requirements.append(f"Frontend: {', '.join(project.tech_stack.frontend)}")
        
        if project.tech_stack.backend:
            requirements.append(f"Backend: {', '.join(project.tech_stack.backend)}")
        
        if project.tech_stack.database:
            requirements.append(f"Database: {', '.join(project.tech_stack.database)}")
        
        # Feature-driven requirements
        feature_text = " ".join([f.feature_name + " " + f.feature_description for f in features]).lower()
        
        if "auth" in feature_text or "login" in feature_text:
            requirements.append("User authentication and session management")
        
        if "payment" in feature_text or "stripe" in feature_text:
            requirements.append("Payment processing integration (PCI compliance)")
        
        if "real-time" in feature_text or "chat" in feature_text:
            requirements.append("Real-time communication infrastructure")
        
        if "search" in feature_text:
            requirements.append("Search and indexing capabilities")
        
        if "file" in feature_text or "upload" in feature_text:
            requirements.append("File storage and management")
        
        # Security and compliance
        requirements.extend([
            "HTTPS/SSL encryption",
            "Data backup and recovery",
            "Basic security measures (input validation, XSS protection)"
        ])
        
        # Performance requirements
        if project.team_size and project.team_size > 3:
            requirements.append("Scalable architecture for team development")
        
        return requirements
    
    def _generate_assumptions(
        self, 
        project: EnhancedProject, 
        features: List[EnhancedFeature],
        url_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate key assumptions for the MVP."""
        
        assumptions = [
            f"Target users ({project.target_users}) have the technical capability to use the platform",
            f"The selected features address the core user needs in the {project.industry.lower()} space",
            "Users are willing to adopt a new solution for their current problem"
        ]
        
        # Tech stack assumptions
        if project.tech_stack.frontend:
            assumptions.append(f"Team has sufficient experience with {project.tech_stack.frontend[0]}")
        
        # Timeline assumptions
        if project.timeline_weeks:
            assumptions.append(f"Development can be completed within {project.timeline_weeks} weeks")
        
        # Market assumptions
        if url_context and url_context.get('business_model'):
            assumptions.append(f"Market demand exists for {url_context['business_model']} solutions in this space")
        
        # Feature assumptions
        high_priority_features = [f for f in features if f.priority == "high"]
        if high_priority_features:
            assumptions.append(f"High-priority features ({', '.join([f.feature_name for f in high_priority_features])}) are correctly identified as most valuable")
        
        return assumptions
    
    def _identify_risks(self, project: EnhancedProject, features: List[EnhancedFeature]) -> List[str]:
        """Identify potential risks for the MVP."""
        
        risks = []
        
        # Technical risks
        complex_features = [f for f in features if f.validation_result and 
                          f.validation_result.get('score', {}).get('complexity_score', 0) > 7]
        
        if complex_features:
            risks.append(f"High complexity features ({', '.join([f.feature_name for f in complex_features])}) may cause timeline delays")
        
        # Team risks
        if project.team_experience == "beginner":
            risks.append("Inexperienced team may face learning curve challenges")
        
        if project.team_size and project.team_size == 1:
            risks.append("Single developer dependency creates bottleneck risk")
        
        # Tech stack risks
        total_tech_count = (len(project.tech_stack.frontend) + len(project.tech_stack.backend) + 
                           len(project.tech_stack.database) + len(project.tech_stack.integrations))
        
        if total_tech_count > 6:
            risks.append("Complex tech stack may increase integration challenges")
        
        # Market risks
        risks.extend([
            "User adoption may be slower than expected",
            "Competitive landscape may change during development",
            "Feature priorities may shift based on user feedback"
        ])
        
        # Feature-specific risks
        feature_text = " ".join([f.feature_description for f in features]).lower()
        
        if "payment" in feature_text:
            risks.append("Payment integration requires PCI compliance and security considerations")
        
        if "real-time" in feature_text:
            risks.append("Real-time features add infrastructure complexity and scaling challenges")
        
        return risks[:6]  # Limit to top 6 risks
    
    def _generate_user_personas(
        self, 
        project: EnhancedProject, 
        features: List[EnhancedFeature],
        url_context: Optional[Dict[str, Any]] = None
    ) -> List[UserPersona]:
        """Generate user personas based on project context."""
        
        personas = []
        
        # Primary persona based on target users
        primary_persona = self._create_primary_persona(project, features, url_context)
        personas.append(primary_persona)
        
        # Secondary persona if applicable
        if project.industry in ["E-COMMERCE", "SOCIAL", "PRODUCTIVITY"]:
            secondary_persona = self._create_secondary_persona(project, features)
            personas.append(secondary_persona)
        
        return personas
    
    def _create_primary_persona(
        self, 
        project: EnhancedProject, 
        features: List[EnhancedFeature],
        url_context: Optional[Dict[str, Any]] = None
    ) -> UserPersona:
        """Create primary user persona."""
        
        # Infer persona details from project
        industry = project.industry
        target_users = project.target_users
        
        if "business" in target_users.lower() or "owner" in target_users.lower():
            name = "Business Owner"
            description = f"Small to medium business owner looking to {self._infer_user_goal(project, features)}"
            pain_points = ["Limited time for complex tools", "Need cost-effective solutions", "Want quick results"]
            goals = ["Increase efficiency", "Reduce costs", "Grow business"]
            tech_savviness = "medium"
        elif "developer" in target_users.lower() or "technical" in target_users.lower():
            name = "Technical User"
            description = f"Developer or technical professional who needs {project.description.lower()}"
            pain_points = ["Complex setup processes", "Poor documentation", "Limited customization"]
            goals = ["Streamline workflow", "Integrate with existing tools", "Maintain control"]
            tech_savviness = "high"
        else:
            name = "Primary User"
            description = target_users
            pain_points = ["Current solutions are too complex", "Lack of suitable options", "Time-consuming processes"]
            goals = ["Solve core problem efficiently", "Easy-to-use solution", "Reliable results"]
            tech_savviness = "medium"
        
        # Generate benefits based on features
        primary_benefits = []
        for feature in features[:3]:  # Top 3 features
            benefit = self._feature_to_user_benefit(feature)
            primary_benefits.append(benefit)
        
        return UserPersona(
            name=name,
            description=description,
            pain_points=pain_points,
            goals=goals,
            tech_savviness=tech_savviness,
            primary_benefits=primary_benefits
        )
    
    def _create_secondary_persona(self, project: EnhancedProject, features: List[EnhancedFeature]) -> UserPersona:
        """Create secondary user persona."""
        
        if project.industry == "E-COMMERCE":
            return UserPersona(
                name="Online Shopper",
                description="End customer who purchases through the e-commerce platform",
                pain_points=["Complicated checkout", "Security concerns", "Limited payment options"],
                goals=["Quick purchases", "Secure transactions", "Good deals"],
                tech_savviness="medium",
                primary_benefits=["Easy shopping experience", "Secure payments", "Fast delivery"]
            )
        elif project.industry == "SOCIAL":
            return UserPersona(
                name="Community Member",
                description="Active participant in the social platform",
                pain_points=["Privacy concerns", "Information overload", "Fake content"],
                goals=["Connect with others", "Share experiences", "Discover content"],
                tech_savviness="medium",
                primary_benefits=["Authentic connections", "Relevant content", "Privacy control"]
            )
        else:
            return UserPersona(
                name="Secondary User",
                description="Additional user type who benefits from the platform",
                pain_points=["Limited access", "Complex interface", "Poor support"],
                goals=["Easy access", "Simple interface", "Reliable support"],
                tech_savviness="low",
                primary_benefits=["Simplified access", "User-friendly design", "Good support"]
            )
    
    def _feature_to_user_benefit(self, feature: EnhancedFeature) -> str:
        """Convert feature to user benefit."""
        name = feature.feature_name.lower()
        
        if "auth" in name or "login" in name:
            return "Secure access to personal account"
        elif "dashboard" in name:
            return "Clear overview of important information"
        elif "search" in name:
            return "Quick discovery of relevant content"
        elif "payment" in name:
            return "Safe and easy transactions"
        elif "profile" in name:
            return "Personalized experience"
        else:
            return f"Access to {feature.feature_name.lower()}"
    
    def _generate_competitive_analysis(
        self, 
        project: EnhancedProject,
        url_context: Optional[Dict[str, Any]] = None
    ) -> CompetitiveAnalysis:
        """Generate competitive analysis."""
        
        direct_competitors = []
        indirect_competitors = []
        market_gaps = []
        differentiation_opportunities = []
        competitive_advantages = []
        
        # Use URL context if available
        if url_context:
            if url_context.get('business_model') == 'ecommerce':
                direct_competitors = ["Shopify", "WooCommerce", "BigCommerce"]
                indirect_competitors = ["Amazon", "Etsy", "Square"]
            elif url_context.get('business_model') == 'saas':
                direct_competitors = ["Existing SaaS platforms", "Enterprise solutions"]
                indirect_competitors = ["Manual processes", "Spreadsheets"]
            elif url_context.get('business_model') == 'social':
                direct_competitors = ["Facebook", "Twitter", "LinkedIn"]
                indirect_competitors = ["Email", "Forums", "Messaging apps"]
        
        # Industry-based competitive landscape
        industry = project.industry
        if industry == "E-COMMERCE":
            if not direct_competitors:
                direct_competitors = ["Shopify", "WooCommerce", "Magento"]
            market_gaps = ["Simplified setup for small businesses", "Industry-specific features"]
            differentiation_opportunities = ["Niche market focus", "Superior user experience", "Better pricing"]
        elif industry == "FINTECH":
            direct_competitors = ["Traditional banks", "Fintech startups", "Payment processors"]
            market_gaps = ["Underserved demographics", "Specific use cases", "Regulatory compliance"]
            differentiation_opportunities = ["Better security", "Lower fees", "Faster processing"]
        elif industry == "PRODUCTIVITY":
            direct_competitors = ["Slack", "Microsoft Teams", "Asana"]
            market_gaps = ["Small team solutions", "Industry-specific workflows"]
            differentiation_opportunities = ["Simpler interface", "Better integrations", "Lower cost"]
        
        # Generic competitive advantages for MVP
        competitive_advantages = [
            "Focused feature set reduces complexity",
            "Faster time-to-market with MVP approach",
            "Lower cost structure enables competitive pricing",
            "Agile development allows rapid iteration"
        ]
        
        return CompetitiveAnalysis(
            direct_competitors=direct_competitors,
            indirect_competitors=indirect_competitors,
            market_gaps=market_gaps,
            differentiation_opportunities=differentiation_opportunities,
            competitive_advantages=competitive_advantages
        )
    
    def _generate_value_proposition(
        self,
        project: EnhancedProject,
        features: List[EnhancedFeature],
        personas: List[UserPersona],
        competitive_analysis: CompetitiveAnalysis,
        url_context: Optional[Dict[str, Any]] = None
    ) -> ValueProposition:
        """Generate comprehensive value proposition."""
        
        # Generate headline
        headline = self._generate_headline(project, features)
        
        # Generate problem statement
        problem_statement = self._generate_problem_statement(project, personas, url_context)
        
        # Generate solution summary
        solution_summary = self._generate_solution_summary(project, features)
        
        # Generate user benefits
        user_benefits = self._generate_user_benefits(features, personas)
        
        # Generate competitive advantages
        competitive_advantages = self._generate_competitive_advantages(
            features, competitive_analysis, project
        )
        
        # Generate success metrics (already done in MVP generation)
        success_metrics = self._generate_success_metrics(project, features)
        
        # Generate user journey value
        user_journey_value = self._generate_user_journey_value(features, personas)
        
        # Generate market positioning
        market_positioning = self._generate_market_positioning(project, competitive_analysis)
        
        # Generate elevator pitch
        elevator_pitch = self._generate_elevator_pitch(headline, problem_statement, solution_summary)
        
        # Calculate confidence score
        confidence_score = self._calculate_value_prop_confidence(project, features, url_context)
        
        return ValueProposition(
            headline=headline,
            problem_statement=problem_statement,
            solution_summary=solution_summary,
            target_user_benefits=user_benefits,
            competitive_advantages=competitive_advantages,
            success_metrics=success_metrics,
            user_journey_value=user_journey_value,
            market_positioning=market_positioning,
            elevator_pitch=elevator_pitch,
            generated_at=datetime.now(),
            confidence_score=confidence_score
        )
    
    def _generate_headline(self, project: EnhancedProject, features: List[EnhancedFeature]) -> str:
        """Generate compelling headline for value proposition."""
        
        industry = project.industry.lower().replace('-', ' ')
        feature_count = len(features)
        
        # Industry-specific headlines
        if "ecommerce" in industry or "e-commerce" in industry:
            return f"Launch your online store with {feature_count} essential features in weeks, not months"
        elif "fintech" in industry:
            return f"Secure financial platform with {feature_count} core features for modern users"
        elif "social" in industry:
            return f"Connect your community with {feature_count} powerful social features"
        elif "productivity" in industry:
            return f"Boost team productivity with {feature_count} streamlined workflow features"
        elif "healthcare" in industry:
            return f"Improve patient outcomes with {feature_count} essential healthcare features"
        elif "education" in industry:
            return f"Transform learning with {feature_count} engaging educational features"
        else:
            return f"Solve your {industry} challenges with {feature_count} focused features"
    
    def _generate_problem_statement(
        self, 
        project: EnhancedProject, 
        personas: List[UserPersona],
        url_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate problem statement."""
        
        primary_persona = personas[0] if personas else None
        
        if primary_persona:
            main_pain_point = primary_persona.pain_points[0] if primary_persona.pain_points else "complex solutions"
            problem = f"{primary_persona.name}s struggle with {main_pain_point.lower()}"
        else:
            problem = f"Users in the {project.industry.lower()} space face complex and inefficient solutions"
        
        # Add context from URL analysis
        if url_context and url_context.get('business_model'):
            problem += f" in the {url_context['business_model']} landscape"
        
        problem += f". Current solutions are either too complex, too expensive, or don't address the specific needs of {project.target_users.lower()}."
        
        return problem
    
    def _generate_solution_summary(self, project: EnhancedProject, features: List[EnhancedFeature]) -> str:
        """Generate solution summary."""
        
        feature_names = [f.feature_name for f in features[:3]]  # Top 3 features
        
        solution = f"{project.name} provides a streamlined solution with {len(features)} core features: {', '.join(feature_names)}. "
        solution += f"Designed specifically for {project.target_users.lower()}, it eliminates complexity while delivering essential functionality. "
        solution += f"Built with modern technology and user-centered design, it offers the perfect balance of power and simplicity."
        
        return solution
    
    def _generate_user_benefits(self, features: List[EnhancedFeature], personas: List[UserPersona]) -> List[UserBenefit]:
        """Generate detailed user benefits."""
        
        benefits = []
        
        for persona in personas:
            # Map persona pain points to feature benefits
            for i, pain_point in enumerate(persona.pain_points[:2]):  # Top 2 pain points
                relevant_features = features[:2] if i == 0 else features[2:4]  # Different features for different pain points
                
                if relevant_features:
                    feature_names = [f.feature_name for f in relevant_features]
                    benefit_text = self._pain_point_to_benefit(pain_point)
                    value_metric = self._benefit_to_metric(benefit_text)
                    
                    benefit = UserBenefit(
                        user_type=persona.name,
                        pain_point=pain_point,
                        benefit=benefit_text,
                        value_metric=value_metric,
                        feature_mapping=feature_names,
                        priority="high" if i == 0 else "medium"
                    )
                    benefits.append(benefit)
        
        return benefits
    
    def _pain_point_to_benefit(self, pain_point: str) -> str:
        """Convert pain point to benefit statement."""
        pain_lower = pain_point.lower()
        
        if "complex" in pain_lower:
            return "Simplified and intuitive user experience"
        elif "time" in pain_lower:
            return "Faster task completion and improved efficiency"
        elif "cost" in pain_lower:
            return "Cost-effective solution with transparent pricing"
        elif "security" in pain_lower:
            return "Enhanced security and data protection"
        elif "integration" in pain_lower:
            return "Seamless integration with existing tools"
        elif "support" in pain_lower:
            return "Reliable customer support and documentation"
        else:
            return f"Solution that addresses {pain_point.lower()}"
    
    def _benefit_to_metric(self, benefit: str) -> str:
        """Convert benefit to measurable metric."""
        benefit_lower = benefit.lower()
        
        if "time" in benefit_lower or "faster" in benefit_lower:
            return "Time saved per task"
        elif "cost" in benefit_lower:
            return "Cost reduction percentage"
        elif "security" in benefit_lower:
            return "Security incident reduction"
        elif "user experience" in benefit_lower:
            return "User satisfaction score"
        elif "efficiency" in benefit_lower:
            return "Productivity improvement"
        else:
            return "User satisfaction improvement"
    
    def _generate_competitive_advantages(
        self, 
        features: List[EnhancedFeature], 
        competitive_analysis: CompetitiveAnalysis,
        project: EnhancedProject
    ) -> List[CompetitiveAdvantage]:
        """Generate competitive advantages."""
        
        advantages = []
        
        # MVP-focused advantages
        mvp_advantage = CompetitiveAdvantage(
            advantage="MVP-First Approach",
            description="Focused feature set that delivers core value without unnecessary complexity",
            supporting_features=[f.feature_name for f in features[:3]],
            market_gap="Over-engineered solutions in the market"
        )
        advantages.append(mvp_advantage)
        
        # Tech stack advantages
        if project.tech_stack.frontend and "React" in project.tech_stack.frontend:
            tech_advantage = CompetitiveAdvantage(
                advantage="Modern Technology Stack",
                description="Built with React and modern web technologies for better performance and user experience",
                supporting_features=[f.feature_name for f in features if "dashboard" in f.feature_name.lower() or "interface" in f.feature_name.lower()],
                market_gap="Legacy technology in existing solutions"
            )
            advantages.append(tech_advantage)
        
        # Industry-specific advantages
        if project.industry == "E-COMMERCE":
            ecommerce_advantage = CompetitiveAdvantage(
                advantage="Small Business Focus",
                description="Designed specifically for small businesses with simplified setup and management",
                supporting_features=[f.feature_name for f in features],
                market_gap="Complex enterprise solutions dominate the market"
            )
            advantages.append(ecommerce_advantage)
        
        # Feature-specific advantages
        auth_features = [f for f in features if "auth" in f.feature_name.lower()]
        if auth_features:
            security_advantage = CompetitiveAdvantage(
                advantage="Security-First Design",
                description="Built-in security features from the ground up",
                supporting_features=[f.feature_name for f in auth_features],
                market_gap="Security often added as an afterthought"
            )
            advantages.append(security_advantage)
        
        return advantages
    
    def _generate_user_journey_value(self, features: List[EnhancedFeature], personas: List[UserPersona]) -> str:
        """Generate user journey value description."""
        
        primary_persona = personas[0] if personas else None
        
        if not primary_persona:
            return "Users experience streamlined workflow from onboarding to goal achievement"
        
        journey_value = f"For {primary_persona.name}s, the platform delivers value at every step: "
        
        # Map features to journey stages
        auth_features = [f for f in features if "auth" in f.feature_name.lower() or "login" in f.feature_name.lower()]
        core_features = [f for f in features if f not in auth_features]
        
        if auth_features:
            journey_value += "secure and simple onboarding, "
        
        if core_features:
            journey_value += f"immediate access to {core_features[0].feature_name.lower()}, "
            if len(core_features) > 1:
                journey_value += f"efficient {core_features[1].feature_name.lower()}, "
        
        journey_value += f"ultimately helping them achieve their primary goal of {primary_persona.goals[0].lower() if primary_persona.goals else 'solving their core problem'}."
        
        return journey_value
    
    def _generate_market_positioning(self, project: EnhancedProject, competitive_analysis: CompetitiveAnalysis) -> str:
        """Generate market positioning statement."""
        
        industry = project.industry.lower().replace('-', ' ')
        
        positioning = f"Positioned as the go-to MVP solution for {project.target_users.lower()} in the {industry} space. "
        
        if competitive_analysis.market_gaps:
            positioning += f"Addresses key market gaps: {', '.join(competitive_analysis.market_gaps[:2])}. "
        
        if competitive_analysis.differentiation_opportunities:
            positioning += f"Differentiates through {competitive_analysis.differentiation_opportunities[0].lower()}. "
        
        positioning += "Targets users who need essential functionality without the complexity of enterprise solutions."
        
        return positioning
    
    def _generate_elevator_pitch(self, headline: str, problem_statement: str, solution_summary: str) -> str:
        """Generate elevator pitch."""
        
        # Extract key elements
        problem_core = problem_statement.split('.')[0]  # First sentence
        solution_core = solution_summary.split('.')[0]  # First sentence
        
        pitch = f"{headline}. {problem_core}, but {solution_core.lower()}. "
        pitch += "Our MVP approach means you get essential features fast, without the complexity and cost of traditional solutions."
        
        return pitch
    
    def _calculate_value_prop_confidence(
        self, 
        project: EnhancedProject, 
        features: List[EnhancedFeature],
        url_context: Optional[Dict[str, Any]] = None
    ) -> float:
        """Calculate confidence score for value proposition."""
        
        confidence = 0.7  # Base confidence
        
        # Higher confidence with more approved features
        approved_features = [f for f in features if f.status == "APPROVED"]
        if len(approved_features) >= 3:
            confidence += 0.1
        
        # Higher confidence with clear target users
        if len(project.target_users) > 20:  # Detailed target user description
            confidence += 0.1
        
        # Higher confidence with URL context
        if url_context:
            confidence += 0.1
        
        # Higher confidence with tech stack defined
        total_tech = (len(project.tech_stack.frontend) + len(project.tech_stack.backend) + 
                     len(project.tech_stack.database))
        if total_tech >= 3:
            confidence += 0.05
        
        # Industry-specific confidence adjustments
        if project.industry in self.industry_templates:
            confidence += 0.05
        
        return min(confidence, 0.95)  # Cap at 95%
