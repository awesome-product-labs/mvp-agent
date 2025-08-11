import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MVPGenerator from './MVPGenerator';

const ProjectDashboard = ({ projectId }) => {
  const [projectData, setProjectData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newFeature, setNewFeature] = useState({
    name: '',
    description: '',
    priority: 'medium',
    user_story: ''
  });
  const [addingFeature, setAddingFeature] = useState(false);
  const [showAddFeature, setShowAddFeature] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (projectId) {
      fetchProjectData();
    }
  }, [projectId]);

  const fetchProjectData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/projects/${projectId}`);
      setProjectData(response.data);
    } catch (err) {
      setError('Failed to load project data');
      console.error('Project fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddFeature = async (e) => {
    e.preventDefault();
    setAddingFeature(true);
    setError('');

    try {
      await axios.post(`/api/v1/projects/${projectId}/features`, newFeature);
      
      // Reset form and refresh data
      setNewFeature({
        name: '',
        description: '',
        priority: 'medium',
        user_story: ''
      });
      setShowAddFeature(false);
      await fetchProjectData();
    } catch (err) {
      setError('Failed to add feature');
      console.error('Add feature error:', err);
    } finally {
      setAddingFeature(false);
    }
  };

  const handleReEvaluateFeature = async (featureId) => {
    try {
      setError('');
      const response = await axios.put(`/api/v1/projects/${projectId}/features/${featureId}/re-evaluate`);
      
      // Show success message
      setError(`✅ Feature re-evaluated successfully! New score: ${response.data.validation_result.score.overall_score}/10`);
      
      // Refresh project data to show updated results
      await fetchProjectData();
      
      // Clear success message after 3 seconds
      setTimeout(() => setError(''), 3000);
    } catch (err) {
      setError('Failed to re-evaluate feature');
      console.error('Re-evaluate feature error:', err);
    }
  };

  const handleGenerateUserStory = async (featureId) => {
    try {
      setError('');
      const response = await axios.post(`/api/v1/projects/${projectId}/features/${featureId}/generate-user-story`);
      
      // Show success message
      setError(`✅ User story generated: "${response.data.user_story}"`);
      
      // Refresh project data to show updated user story
      await fetchProjectData();
      
      // Clear success message after 5 seconds
      setTimeout(() => setError(''), 5000);
    } catch (err) {
      setError('Failed to generate user story');
      console.error('Generate user story error:', err);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'APPROVED': 'bg-green-100 text-green-800',
      'PENDING': 'bg-yellow-100 text-yellow-800',
      'REJECTED': 'bg-red-100 text-red-800',
      'IN_DEVELOPMENT': 'bg-blue-100 text-blue-800',
      'COMPLETED': 'bg-purple-100 text-purple-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'high': 'bg-red-100 text-red-800',
      'medium': 'bg-yellow-100 text-yellow-800',
      'low': 'bg-green-100 text-green-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  const getDecisionColor = (decision) => {
    const colors = {
      'ACCEPT': 'text-green-600',
      'MODIFY': 'text-yellow-600',
      'DEFER': 'text-blue-600',
      'REJECT': 'text-red-600'
    };
    return colors[decision] || 'text-gray-600';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!projectData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No project selected</p>
      </div>
    );
  }

  const { project, features, analysis, url_context } = projectData;

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Project Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
            <p className="text-gray-600 mt-2">{project.description}</p>
          </div>
          <div className="text-right">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
              {project.status}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Industry</h3>
            <p className="text-lg font-semibold text-gray-900">{project.industry}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Timeline</h3>
            <p className="text-lg font-semibold text-gray-900">{project.timeline_weeks || 'N/A'} weeks</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Team Size</h3>
            <p className="text-lg font-semibold text-gray-900">{project.team_size || 'N/A'}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Features</h3>
            <p className="text-lg font-semibold text-gray-900">{project.total_features}</p>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white rounded-lg shadow-lg">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'overview'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📊 Overview
            </button>
            <button
              onClick={() => setActiveTab('features')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'features'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              🔧 Features
            </button>
            <button
              onClick={() => setActiveTab('mvp')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'mvp'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              🚀 Generate MVP
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'mvp' && (
            <MVPGenerator project={project} features={features} />
          )}
          
          {activeTab === 'features' && (
            <div className="space-y-6">
              {/* Features Section */}
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Features</h2>
                <button
                  onClick={() => setShowAddFeature(!showAddFeature)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Add Feature
                </button>
              </div>

              {/* Add Feature Form */}
              {showAddFeature && (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <form onSubmit={handleAddFeature} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Feature Name *
                        </label>
                        <input
                          type="text"
                          value={newFeature.name}
                          onChange={(e) => setNewFeature(prev => ({ ...prev, name: e.target.value }))}
                          required
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          placeholder="e.g., User Dashboard"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Priority
                        </label>
                        <select
                          value={newFeature.priority}
                          onChange={(e) => setNewFeature(prev => ({ ...prev, priority: e.target.value }))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value="high">High</option>
                          <option value="medium">Medium</option>
                          <option value="low">Low</option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Description *
                      </label>
                      <textarea
                        value={newFeature.description}
                        onChange={(e) => setNewFeature(prev => ({ ...prev, description: e.target.value }))}
                        required
                        rows={3}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Describe the feature and its functionality..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        User Story
                      </label>
                      <textarea
                        value={newFeature.user_story}
                        onChange={(e) => setNewFeature(prev => ({ ...prev, user_story: e.target.value }))}
                        rows={2}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="As a [user], I want [goal] so that [benefit]..."
                      />
                    </div>

                    <div className="flex justify-end space-x-2">
                      <button
                        type="button"
                        onClick={() => setShowAddFeature(false)}
                        className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={addingFeature}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
                      >
                        {addingFeature ? 'Adding...' : 'Add Feature'}
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Features List */}
              <div className="space-y-4">
                {features.map((feature) => (
                  <div key={feature.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900">{feature.feature_name}</h3>
                        <p className="text-gray-600 mt-1">{feature.feature_description}</p>
                        {feature.user_story && (
                          <p className="text-sm text-blue-600 mt-2 italic">{feature.user_story}</p>
                        )}
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(feature.status)}`}>
                          {feature.status}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(feature.priority)}`}>
                          {feature.priority}
                        </span>
                      </div>
                    </div>

                    {feature.validation_result && (
                      <div className="bg-gray-50 rounded-lg p-3 mt-3">
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="font-medium text-gray-900">Validation Result</h4>
                          <span className={`font-semibold ${getDecisionColor(feature.validation_result.decision)}`}>
                            {feature.validation_result.decision}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                          <div>
                            <span className="text-xs text-gray-500">MVP Score</span>
                            <p className="font-semibold">{feature.validation_result.score.core_mvp_score}/10</p>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500">Complexity</span>
                            <p className="font-semibold">{feature.validation_result.score.complexity_score}/10</p>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500">User Value</span>
                            <p className="font-semibold">{feature.validation_result.score.user_value_score}/10</p>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500">Timeline</span>
                            <p className="font-semibold">{feature.estimated_weeks}w</p>
                          </div>
                        </div>

                        <p className="text-sm text-gray-700 mb-3">{feature.validation_result.rationale}</p>
                        
                        {feature.validation_result.alternatives.length > 0 && (
                          <div className="mb-3">
                            <span className="text-xs font-medium text-gray-500">Alternatives:</span>
                            <ul className="text-sm text-gray-600 mt-1">
                              {feature.validation_result.alternatives.map((alt, index) => (
                                <li key={index}>• {alt}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Action Buttons */}
                        <div className="flex space-x-2 pt-2 border-t border-gray-200">
                          <button
                            onClick={() => handleReEvaluateFeature(feature.id)}
                            className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                          >
                            🔄 Re-evaluate
                          </button>
                          {!feature.user_story && (
                            <button
                              onClick={() => handleGenerateUserStory(feature.id)}
                              className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                            >
                              ✨ Generate User Story
                            </button>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {features.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500">No features added yet. Click "Add Feature" to get started.</p>
                </div>
              )}
            </div>
          )}
          
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Project Analysis */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Project Analysis</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="text-sm font-medium text-blue-600">MVP Readiness</h3>
                    <div className="flex items-center mt-2">
                      <div className="flex-1 bg-blue-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${analysis.mvp_readiness * 10}%` }}
                        ></div>
                      </div>
                      <span className="text-lg font-semibold text-blue-900">
                        {analysis.mvp_readiness.toFixed(1)}/10
                      </span>
                    </div>
                  </div>

                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h3 className="text-sm font-medium text-yellow-600">Complexity Score</h3>
                    <div className="flex items-center mt-2">
                      <div className="flex-1 bg-yellow-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-yellow-600 h-2 rounded-full" 
                          style={{ width: `${analysis.complexity_score * 10}%` }}
                        ></div>
                      </div>
                      <span className="text-lg font-semibold text-yellow-900">
                        {analysis.complexity_score.toFixed(1)}/10
                      </span>
                    </div>
                  </div>

                  <div className="bg-green-50 p-4 rounded-lg">
                    <h3 className="text-sm font-medium text-green-600">Estimated Timeline</h3>
                    <p className="text-lg font-semibold text-green-900 mt-2">
                      {analysis.estimated_timeline ? `${analysis.estimated_timeline} weeks` : 'TBD'}
                    </p>
                  </div>
                </div>

                {/* Recommendations and Risks */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {analysis.recommendations.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">Recommendations</h3>
                      <ul className="space-y-2">
                        {analysis.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {analysis.risk_factors.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">Risk Factors</h3>
                      <ul className="space-y-2">
                        {analysis.risk_factors.map((risk, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-red-500 mr-2">⚠</span>
                            <span className="text-gray-700">{risk}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              {/* URL Context Analysis */}
              {url_context && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Reference System Analysis</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">System Overview</h3>
                      <div className="space-y-2">
                        <p><span className="font-medium">Business Model:</span> {url_context.business_model}</p>
                        <p><span className="font-medium">Target Audience:</span> {url_context.target_audience}</p>
                        {url_context.tech_stack.length > 0 && (
                          <div>
                            <span className="font-medium">Tech Stack:</span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {url_context.tech_stack.map((tech, index) => (
                                <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                                  {tech}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Features</h3>
                      <ul className="space-y-1">
                        {url_context.extracted_features.map((feature, index) => (
                          <li key={index} className="text-gray-700">• {feature}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {/* Development Phases */}
              {analysis.suggested_phases.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Suggested Development Phases</h2>
                  <div className="space-y-4">
                    {analysis.suggested_phases.map((phase, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex justify-between items-center mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            Phase {phase.phase}: {phase.name}
                          </h3>
                          <span className="text-sm text-gray-500">
                            {phase.estimated_weeks} weeks
                          </span>
                        </div>
                        <p className="text-gray-600 mb-3">{phase.description}</p>
                        <div>
                          <span className="text-sm font-medium text-gray-700">Features:</span>
                          <ul className="text-sm text-gray-600 mt-1">
                            {phase.features.map((featureName, idx) => (
                              <li key={idx}>• {featureName}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectDashboard;
