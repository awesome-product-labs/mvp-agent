import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Send, Loader2, AlertCircle } from 'lucide-react';
import axios from 'axios';
import ValidationResult from './ValidationResult';

const FeatureValidator = () => {
  const [validationResult, setValidationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch
  } = useForm({
    defaultValues: {
      name: '',
      description: '',
      user_story: '',
      acceptance_criteria: '',
      priority: 'medium'
    }
  });

  const watchedDescription = watch('description');

  const generateUserStoryFromForm = async () => {
    const name = watch('name');
    const description = watch('description');
    
    if (!name || !description) {
      setError('Please fill in feature name and description first');
      return;
    }

    try {
      // For now, generate a simple user story template
      // In a real implementation, this would call the API
      const userStory = `As a user, I want to use ${name.toLowerCase()} so that I can ${description.toLowerCase().substring(0, 50)}...`;
      
      // Update the form field
      const currentValues = watch();
      reset({
        ...currentValues,
        user_story: userStory
      });
      
    } catch (err) {
      setError('Failed to generate user story');
    }
  };

  const onSubmit = async (data) => {
    setIsLoading(true);
    setError(null);
    setValidationResult(null);

    try {
      // Process acceptance criteria into array
      const acceptanceCriteria = data.acceptance_criteria
        ? data.acceptance_criteria.split('\n').filter(item => item.trim())
        : [];

      const payload = {
        ...data,
        acceptance_criteria: acceptanceCriteria
      };

      const response = await axios.post('/api/v1/validate-feature', payload);
      setValidationResult(response.data);
    } catch (err) {
      console.error('Validation error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to validate feature. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    reset();
    setValidationResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gradient mb-4">
          Feature Validator
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Submit your feature idea and get AI-powered analysis on its MVP suitability, 
          complexity, and user value. Get instant recommendations and alternatives.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Feature Name */}
            <div>
              <label className="label">
                Feature Name *
              </label>
              <input
                type="text"
                className="input"
                placeholder="e.g., User Authentication System"
                {...register('name', { 
                  required: 'Feature name is required',
                  minLength: { value: 3, message: 'Name must be at least 3 characters' }
                })}
              />
              {errors.name && (
                <p className="error-text">{errors.name.message}</p>
              )}
            </div>

            {/* Feature Description */}
            <div>
              <label className="label">
                Feature Description *
              </label>
              <textarea
                rows={4}
                className="textarea"
                placeholder="Describe the feature in detail. What does it do? How does it work?"
                {...register('description', { 
                  required: 'Feature description is required',
                  minLength: { value: 20, message: 'Description must be at least 20 characters' }
                })}
              />
              {errors.description && (
                <p className="error-text">{errors.description.message}</p>
              )}
              <div className="text-xs text-gray-500 mt-1">
                {watchedDescription?.length || 0} characters
              </div>
            </div>

            {/* User Story */}
            <div>
              <label className="label">
                User Story (Optional)
              </label>
              <div className="relative">
                <textarea
                  rows={2}
                  className="textarea"
                  placeholder="As a [user type], I want [functionality] so that [benefit]"
                  {...register('user_story')}
                />
                <button
                  type="button"
                  onClick={() => generateUserStoryFromForm()}
                  className="absolute top-2 right-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                  title="Generate user story from feature description"
                >
                  ✨ Generate
                </button>
              </div>
            </div>

            {/* Acceptance Criteria */}
            <div>
              <label className="label">
                Acceptance Criteria (Optional)
              </label>
              <textarea
                rows={3}
                className="textarea"
                placeholder="Enter each criterion on a new line:&#10;- User can log in with email and password&#10;- System validates credentials&#10;- Invalid attempts are logged"
                {...register('acceptance_criteria')}
              />
              <div className="text-xs text-gray-500 mt-1">
                Enter each criterion on a new line
              </div>
            </div>

            {/* Priority */}
            <div>
              <label className="label">
                Priority Level
              </label>
              <select
                className="input"
                {...register('priority')}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            {/* Error Display */}
            {error && (
              <div className="flex items-center space-x-2 p-3 bg-danger-50 border border-danger-200 rounded-lg">
                <AlertCircle className="h-5 w-5 text-danger-600" />
                <p className="text-danger-700">{error}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary flex-1 flex items-center justify-center space-x-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    <span>Validate Feature</span>
                  </>
                )}
              </button>
              
              <button
                type="button"
                onClick={handleReset}
                className="btn-secondary"
                disabled={isLoading}
              >
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {isLoading && (
            <div className="card">
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto mb-4" />
                  <p className="text-gray-600">Analyzing your feature...</p>
                  <p className="text-sm text-gray-500 mt-2">
                    This may take a few seconds
                  </p>
                </div>
              </div>
            </div>
          )}

          {validationResult && !isLoading && (
            <ValidationResult data={validationResult} />
          )}

          {!validationResult && !isLoading && !error && (
            <div className="card">
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <Send className="h-12 w-12 mx-auto" />
                </div>
                <p className="text-gray-600">
                  Submit a feature to see validation results
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Get AI-powered analysis on MVP suitability, complexity, and recommendations
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FeatureValidator;
