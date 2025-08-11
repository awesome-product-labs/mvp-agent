"""
API routes for MVP feature validation.
"""
import logging
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from .models import (
    FeatureRequest,
    FeatureValidationResponse,
    ErrorResponse,
    HealthResponse
)
from ..agent.validators import MVPFeatureValidator, ValidationCache
from ..utils.claude_client import ClaudeClient

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Global instances (in production, use dependency injection)
validation_cache = ValidationCache()
validator = None


def get_validator() -> MVPFeatureValidator:
    """Dependency to get validator instance."""
    global validator
    if validator is None:
        try:
            # Try to initialize with real Claude client
            claude_client = ClaudeClient()
            validator = MVPFeatureValidator(claude_client)
        except Exception as e:
            logger.warning(f"Failed to initialize Claude client: {str(e)}")
            logger.info("Falling back to mock client for testing")
            # Import mock client for fallback
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from test_mvp_agent import MockClaudeClient
            mock_client = MockClaudeClient()
            validator = MVPFeatureValidator(mock_client)
    return validator


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@router.post("/validate-feature", response_model=FeatureValidationResponse)
async def validate_feature(
    feature_request: FeatureRequest,
    validator: MVPFeatureValidator = Depends(get_validator)
):
    """
    Validate a feature request for MVP inclusion.
    
    Args:
        feature_request: The feature to validate
        validator: The validator instance
        
    Returns:
        Validation result with decision and analysis
    """
    start_time = time.time()
    
    try:
        logger.info(f"Received validation request for feature: {feature_request.name}")
        
        # Check cache first
        cache_key = validation_cache.generate_key(feature_request)
        cached_result = validation_cache.get(cache_key)
        
        if cached_result:
            logger.info("Returning cached validation result")
            processing_time = time.time() - start_time
            return FeatureValidationResponse(
                feature=feature_request,
                result=cached_result,
                timestamp=datetime.now().isoformat(),
                processing_time=processing_time
            )
        
        # Perform validation
        result = await validator.validate_feature(feature_request)
        
        # Cache the result
        validation_cache.set(cache_key, result)
        
        processing_time = time.time() - start_time
        logger.info(f"Validation completed in {processing_time:.2f}s with decision: {result.decision}")
        
        return FeatureValidationResponse(
            feature=feature_request,
            result=result,
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Validation failed after {processing_time:.2f}s: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )


@router.post("/validate-batch")
async def validate_batch_features(
    features: list[FeatureRequest],
    validator: MVPFeatureValidator = Depends(get_validator)
):
    """
    Validate multiple features in batch.
    
    Args:
        features: List of features to validate
        validator: The validator instance
        
    Returns:
        List of validation results
    """
    if len(features) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 features allowed per batch request"
        )
    
    start_time = time.time()
    results = []
    
    try:
        for feature in features:
            # Check cache first
            cache_key = validation_cache.generate_key(feature)
            cached_result = validation_cache.get(cache_key)
            
            if cached_result:
                result = cached_result
            else:
                result = await validator.validate_feature(feature)
                validation_cache.set(cache_key, result)
            
            results.append(FeatureValidationResponse(
                feature=feature,
                result=result,
                timestamp=datetime.now().isoformat(),
                processing_time=0  # Individual timing not tracked in batch
            ))
        
        processing_time = time.time() - start_time
        logger.info(f"Batch validation of {len(features)} features completed in {processing_time:.2f}s")
        
        return {
            "results": results,
            "total_features": len(features),
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Batch validation failed after {processing_time:.2f}s: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Batch validation failed: {str(e)}"
        )


@router.get("/validation-stats")
async def get_validation_stats():
    """Get validation statistics and cache info."""
    return {
        "cache_size": len(validation_cache.cache),
        "cache_max_size": validation_cache.max_size,
        "timestamp": datetime.now().isoformat()
    }


@router.delete("/cache")
async def clear_cache():
    """Clear the validation cache."""
    global validation_cache
    validation_cache = ValidationCache()
    return {
        "message": "Cache cleared successfully",
        "timestamp": datetime.now().isoformat()
    }
