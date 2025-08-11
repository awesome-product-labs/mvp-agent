#!/usr/bin/env python3
"""
Test script for MVP Generation Agent
This script demonstrates the feature validation functionality without requiring a Claude API key.
"""

import asyncio
import json
from datetime import datetime
from src.api.models import FeatureRequest, ValidationResult, ValidationScore, ValidationDecision


class MockClaudeClient:
    """Mock Claude client for testing without API key."""
    
    async def analyze_feature(self, feature_description: str, context: dict = None) -> dict:
        """Mock analysis that provides realistic responses based on feature complexity."""
        
        # Simple heuristics to simulate AI analysis
        description_lower = feature_description.lower()
        
        # Determine complexity based on keywords
        complexity_keywords = [
            'machine learning', 'ai', 'blockchain', 'real-time', 'analytics',
            'recommendation', 'personalization', 'integration', 'api', 'microservices'
        ]
        
        mvp_keywords = [
            'login', 'register', 'profile', 'basic', 'simple', 'crud',
            'list', 'view', 'create', 'edit', 'delete'
        ]
        
        complexity_score = 3  # Base complexity
        for keyword in complexity_keywords:
            if keyword in description_lower:
                complexity_score += 2
        
        mvp_score = 5  # Base MVP score
        for keyword in mvp_keywords:
            if keyword in description_lower:
                mvp_score += 1
        
        # Cap scores at 10
        complexity_score = min(complexity_score, 10)
        mvp_score = min(mvp_score, 10)
        
        # User value based on description length and keywords
        user_value_score = min(6 + len(feature_description) // 50, 10)
        
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
            "decision": decision,
            "rationale": rationale,
            "alternatives": alternatives,
            "timeline_impact": "2-4 weeks" if complexity_score <= 5 else "4-8 weeks" if complexity_score <= 8 else "8+ weeks",
            "dependencies": ["Authentication system"] if "login" in description_lower or "user" in description_lower else []
        }


async def test_feature_validation():
    """Test the feature validation system with various examples."""
    
    # Import here to avoid issues with missing API key
    from src.agent.validators import MVPFeatureValidator
    
    # Create mock client and validator
    mock_client = MockClaudeClient()
    validator = MVPFeatureValidator(claude_client=mock_client)
    
    # Test features
    test_features = [
        {
            "name": "User Authentication",
            "description": "Allow users to register, login, and manage their profiles with email and password authentication.",
            "priority": "high"
        },
        {
            "name": "AI-Powered Recommendation Engine",
            "description": "Implement a machine learning system that analyzes user behavior patterns, preferences, and historical data to provide personalized content recommendations with real-time A/B testing capabilities.",
            "priority": "medium"
        },
        {
            "name": "Basic Task Management",
            "description": "Users can create, edit, delete, and view tasks in a simple list format with due dates and priority levels.",
            "priority": "high"
        },
        {
            "name": "Advanced Analytics Dashboard",
            "description": "Comprehensive analytics dashboard with real-time data visualization, custom reporting, predictive analytics, and integration with multiple third-party services.",
            "priority": "low"
        }
    ]
    
    print("🚀 MVP Generation Agent - Feature Validation Test")
    print("=" * 60)
    
    for i, feature_data in enumerate(test_features, 1):
        print(f"\n📋 Test {i}: {feature_data['name']}")
        print("-" * 40)
        
        # Create feature request
        feature_request = FeatureRequest(
            name=feature_data["name"],
            description=feature_data["description"],
            priority=feature_data["priority"]
        )
        
        # Validate feature
        try:
            result = await validator.validate_feature(feature_request)
            
            # Display results
            print(f"Decision: {result.decision.value}")
            print(f"Scores:")
            print(f"  • MVP Essentiality: {result.score.core_mvp_score}/10")
            print(f"  • User Value: {result.score.user_value_score}/10")
            print(f"  • Complexity: {result.score.complexity_score}/10")
            print(f"  • Overall: {result.score.overall_score}/10")
            print(f"Confidence: {int(result.confidence * 100)}%")
            print(f"Timeline: {result.timeline_impact}")
            print(f"Rationale: {result.rationale}")
            
            if result.alternatives:
                print("Alternatives:")
                for alt in result.alternatives:
                    print(f"  • {alt}")
            
            if result.dependencies:
                print("Dependencies:")
                for dep in result.dependencies:
                    print(f"  • {dep}")
                    
        except Exception as e:
            print(f"❌ Error validating feature: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Feature validation test completed!")
    print("\nTo use with real Claude API:")
    print("1. Get a Claude API key from Anthropic")
    print("2. Update ANTHROPIC_API_KEY in backend/.env")
    print("3. Run: cd backend && source venv/bin/activate && python -m uvicorn src.api.main:app --reload")


async def test_api_models():
    """Test the API models and data structures."""
    
    print("\n🔧 Testing API Models")
    print("-" * 30)
    
    # Test feature request creation
    feature = FeatureRequest(
        name="Test Feature",
        description="A test feature for validation",
        user_story="As a user, I want to test the system so that I can verify it works",
        acceptance_criteria=["Feature works correctly", "No errors occur"],
        priority="medium"
    )
    
    print(f"✅ Created FeatureRequest: {feature.name}")
    
    # Test validation score
    score = ValidationScore(
        core_mvp_score=8.0,
        complexity_score=4.0,
        user_value_score=7.0,
        overall_score=6.8
    )
    
    print(f"✅ Created ValidationScore: Overall {score.overall_score}/10")
    
    # Test validation result
    result = ValidationResult(
        decision=ValidationDecision.ACCEPT,
        score=score,
        rationale="This is a test validation result",
        alternatives=["Alternative 1", "Alternative 2"],
        timeline_impact="2-3 weeks",
        dependencies=["Test dependency"],
        confidence=0.85
    )
    
    print(f"✅ Created ValidationResult: {result.decision.value}")
    print("✅ All API models working correctly!")


if __name__ == "__main__":
    print("🎯 MVP Generation Agent - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_api_models())
    asyncio.run(test_feature_validation())
    
    print(f"\n📊 Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nNext steps:")
    print("1. Install Node.js to run the React frontend")
    print("2. Get a Claude API key for real AI analysis")
    print("3. Start the FastAPI server: uvicorn src.api.main:app --reload")
    print("4. Start the React frontend: npm run dev")
