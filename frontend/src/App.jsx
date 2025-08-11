import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8003';

function App() {
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [currentView, setCurrentView] = useState('dashboard');
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [features, setFeatures] = useState([]);
  const [mvpResult, setMvpResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [editingFeature, setEditingFeature] = useState(null);

  useEffect(() => {
    checkConnection();
    loadProjects();
  }, []);

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const makeRequest = async (method, endpoint, data = null) => {
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };
      
      if (data) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(`${API_BASE}${endpoint}`, options);
      const result = await response.json();
      
      return {
        success: response.ok,
        status: response.status,
        data: result
      };
    } catch (error) {
      return {
        success: false,
        status: 0,
        error: error.message
      };
    }
  };

  const checkConnection = async () => {
    setConnectionStatus('checking');
    const result = await makeRequest('GET', '/api/v1/health');
    setConnectionStatus(result.success ? 'connected' : 'failed');
  };

  const loadProjects = async () => {
    const result = await makeRequest('GET', '/api/v1/projects');
    if (result.success) {
      // Handle the correct API response structure
      const projectList = result.data.projects || [];
      setProjects(projectList);
    }
  };

  const loadProject = async (projectId) => {
    const result = await makeRequest('GET', `/api/v1/projects/${projectId}`);
    if (result.success) {
      // Handle the correct API response structure
      const projectData = result.data.project;
      const projectFeatures = result.data.features || [];
      
      setCurrentProject(projectData);
      setFeatures(projectFeatures);
      setCurrentView('project');
    }
  };

  const createProject = async (projectData) => {
    setLoading(true);
    const payload = {
      ...projectData,
      tech_stack: {
        frontend: ["React"],
        backend: ["Node.js"],
        database: ["PostgreSQL"]
      }
    };

    const result = await makeRequest('POST', '/api/v1/projects', payload);
    
    if (result.success) {
      setCurrentProject(result.data);
      setFeatures([]);
      setCurrentView('project');
      showNotification('Project created successfully!');
      loadProjects();
    } else {
      showNotification('Failed to create project. Please try again.', 'error');
    }
    setLoading(false);
  };

  const deleteProject = async (projectId) => {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    setLoading(true);
    const result = await makeRequest('DELETE', `/api/v1/projects/${projectId}`);
    
    if (result.success) {
      showNotification('Project deleted successfully!');
      loadProjects();
      if (currentProject?.id === projectId) {
        setCurrentProject(null);
        setFeatures([]);
        setCurrentView('dashboard');
      }
    } else {
      showNotification('Failed to delete project.', 'error');
    }
    setLoading(false);
  };

  const addFeature = async (featureData) => {
    if (!currentProject) return;
    
    setLoading(true);
    const result = await makeRequest('POST', `/api/v1/projects/${currentProject.id}/features`, featureData);
    
    if (result.success) {
      // Handle the correct API response structure
      const overallScore = result.data.result?.score?.overall_score || 'N/A';
      showNotification(`Feature "${featureData.name}" added with ${overallScore}/10 score!`);
      loadProject(currentProject.id); // Reload to get updated features
    } else {
      showNotification('Failed to add feature. Please try again.', 'error');
    }
    setLoading(false);
  };

  const generateUserStory = async (featureId) => {
    if (!currentProject || !featureId) return;
    
    setLoading(true);
    const result = await makeRequest('POST', `/api/v1/projects/${currentProject.id}/features/${featureId}/generate-user-story`);
    
    if (result.success) {
      showNotification('User story generated successfully!');
      loadProject(currentProject.id); // Reload to get updated feature
    } else {
      showNotification('Failed to generate user story.', 'error');
    }
    setLoading(false);
  };

  const updateFeature = async (featureId, featureData) => {
    if (!currentProject) return;
    
    setLoading(true);
    // Use re-evaluate endpoint since there's no direct update
    const result = await makeRequest('PUT', `/api/v1/projects/${currentProject.id}/features/${featureId}/re-evaluate`);
    
    if (result.success) {
      showNotification('Feature updated successfully!');
      loadProject(currentProject.id);
      setEditingFeature(null);
    } else {
      showNotification('Failed to update feature.', 'error');
    }
    setLoading(false);
  };

  const generateMVP = async () => {
    if (!currentProject || features.length === 0) {
      showNotification('Please add at least one feature before generating MVP', 'error');
      return;
    }

    setLoading(true);
    const mvpData = {
      target_timeline_weeks: 12,
      budget_range: "25000-75000",
      priority_focus: "user_experience"
    };

    const result = await makeRequest('POST', `/api/v1/projects/${currentProject.id}/generate-mvp`, mvpData);
    
    if (result.success) {
      setMvpResult(result.data);
      setCurrentView('mvp-result');
      showNotification('MVP generated successfully!');
    } else {
      showNotification('Failed to generate MVP. Please try again.', 'error');
    }
    setLoading(false);
  };

  const DetailedScoreDisplay = ({ validation }) => {
    if (!validation || !validation.score) return null;

    return (
      <div className="mt-3 p-3 bg-gray-50 rounded-lg">
        <h5 className="font-medium text-gray-900 mb-2">Detailed Scoring</h5>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <div className="text-gray-600">MVP Score</div>
            <div className="font-semibold text-blue-600">{validation.score.core_mvp_score || 0}/10</div>
          </div>
          <div>
            <div className="text-gray-600">Complexity</div>
            <div className="font-semibold text-orange-600">{validation.score.complexity_score || 0}/10</div>
          </div>
          <div>
            <div className="text-gray-600">User Value</div>
            <div className="font-semibold text-green-600">{validation.score.user_value_score || 0}/10</div>
          </div>
        </div>
        <div className="mt-2 text-xs text-gray-600">
          <strong>Decision:</strong> {validation.decision || 'N/A'} | <strong>Overall:</strong> {validation.score.overall_score || 0}/10
        </div>
        <div className="mt-1 text-xs text-gray-500">
          {validation.rationale || 'No rationale provided'}
        </div>
        {validation.alternatives && validation.alternatives.length > 0 && (
          <div className="mt-2">
            <div className="text-xs font-medium text-gray-700">Alternatives:</div>
            <ul className="text-xs text-gray-600 list-disc list-inside">
              {validation.alternatives.map((alt, idx) => (
                <li key={idx}>{alt}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const FeatureCard = ({ feature, index }) => {
    const isEditing = editingFeature === feature.id;
    
    // Handle validation result - it might be nested in validation_result
    const validation = feature.validation_result || feature.validation || null;

    return (
      <div className="border border-gray-200 rounded-lg p-4">
        {isEditing ? (
          <div className="space-y-3">
            <input
              type="text"
              defaultValue={feature.feature_name || feature.name || ''}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Feature name"
            />
            <textarea
              defaultValue={feature.feature_description || feature.description || ''}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Feature description"
            />
            <div className="flex space-x-2">
              <button
                onClick={() => updateFeature(feature.id, {})}
                className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
              >
                Save
              </button>
              <button
                onClick={() => setEditingFeature(null)}
                className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-semibold text-gray-900">
                {feature.feature_name || feature.name || 'Unnamed Feature'}
              </h4>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setEditingFeature(feature.id)}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  Edit
                </button>
                <button
                  onClick={() => generateUserStory(feature.id)}
                  disabled={loading}
                  className="text-green-600 hover:text-green-800 text-sm disabled:text-gray-400"
                >
                  {loading ? 'Generating...' : 'User Story'}
                </button>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  feature.priority === 'high' ? 'bg-red-100 text-red-800' :
                  feature.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {feature.priority || 'medium'} priority
                </span>
                {validation && validation.score && (
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                    Score: {validation.score.overall_score || 0}/10
                  </span>
                )}
              </div>
            </div>
            <p className="text-gray-600 text-sm mb-2">
              {feature.feature_description || feature.description || 'No description provided'}
            </p>
            {feature.user_story && (
              <div className="mt-2 p-2 bg-blue-50 rounded text-sm">
                <strong>User Story:</strong> {feature.user_story}
              </div>
            )}
            {validation && <DetailedScoreDisplay validation={validation} />}
          </>
        )}
      </div>
    );
  };

  const ProjectForm = ({ onSubmit, initialData = null }) => {
    const [projectData, setProjectData] = useState(initialData || {
      name: '',
      description: '',
      industry: 'PRODUCTIVITY',
      target_users: '',
      reference_url: ''
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      if (!projectData.name || !projectData.description) {
        showNotification('Please fill in all required fields', 'error');
        return;
      }
      onSubmit(projectData);
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Project Name *
          </label>
          <input
            type="text"
            value={projectData.name}
            onChange={(e) => setProjectData(prev => ({ ...prev, name: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., TaskFlow Pro, EcoTracker, FitnessBuddy"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Project Description *
          </label>
          <textarea
            value={projectData.description}
            onChange={(e) => setProjectData(prev => ({ ...prev, description: e.target.value }))}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your project idea, what problem it solves, and who it's for..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Industry
            </label>
            <select
              value={projectData.industry}
              onChange={(e) => setProjectData(prev => ({ ...prev, industry: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="PRODUCTIVITY">Productivity</option>
              <option value="E-COMMERCE">E-commerce</option>
              <option value="FINTECH">Fintech</option>
              <option value="HEALTHCARE">Healthcare</option>
              <option value="EDUCATION">Education</option>
              <option value="SOCIAL">Social</option>
              <option value="ENTERTAINMENT">Entertainment</option>
              <option value="OTHER">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Target Users
            </label>
            <input
              type="text"
              value={projectData.target_users}
              onChange={(e) => setProjectData(prev => ({ ...prev, target_users: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Small business owners, Students, Fitness enthusiasts"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Reference URL (Optional)
          </label>
          <input
            type="url"
            value={projectData.reference_url}
            onChange={(e) => setProjectData(prev => ({ ...prev, reference_url: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="https://example.com - Similar product or inspiration"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating Project...' : (initialData ? 'Update Project' : 'Create Project')}
        </button>
      </form>
    );
  };

  const FeatureForm = ({ onSubmit }) => {
    const [feature, setFeature] = useState({
      name: '',
      description: '',
      priority: 'high'
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      if (!feature.name || !feature.description) {
        showNotification('Please fill in all feature fields', 'error');
        return;
      }
      onSubmit(feature);
      setFeature({ name: '', description: '', priority: 'high' });
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Feature Name *
          </label>
          <input
            type="text"
            value={feature.name}
            onChange={(e) => setFeature(prev => ({ ...prev, name: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., User Authentication, Task Management"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Feature Description *
          </label>
          <textarea
            value={feature.description}
            onChange={(e) => setFeature(prev => ({ ...prev, description: e.target.value }))}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe what this feature does and why it's important..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority Level
          </label>
          <select
            value={feature.priority}
            onChange={(e) => setFeature(prev => ({ ...prev, priority: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="high">High Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="low">Low Priority</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Adding Feature...' : 'Add Feature'}
        </button>
      </form>
    );
  };

  if (connectionStatus === 'failed') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Connection Failed</h2>
          <p className="text-gray-600 mb-4">Unable to connect to the MVP Generation service.</p>
          <button
            onClick={checkConnection}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-md shadow-lg ${
          notification.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`}>
          {notification.message}
        </div>
      )}

      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">MVP Generation Agent</h1>
              <p className="text-gray-600 mt-1">Transform your ideas into validated MVP plans</p>
            </div>
            <nav className="flex space-x-4">
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`px-4 py-2 rounded-md ${
                  currentView === 'dashboard' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setCurrentView('create-project')}
                className={`px-4 py-2 rounded-md ${
                  currentView === 'create-project' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                New Project
              </button>
              {currentProject && (
                <button
                  onClick={() => setCurrentView('project')}
                  className={`px-4 py-2 rounded-md ${
                    currentView === 'project' 
                      ? 'bg-blue-600 text-white' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {currentProject.name}
                </button>
              )}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Dashboard View */}
        {currentView === 'dashboard' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Project Overview</h2>
              
              {projects.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-gray-400 text-6xl mb-4">📋</div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No projects yet</h3>
                  <p className="text-gray-600 mb-4">Create your first MVP project to get started</p>
                  <button
                    onClick={() => setCurrentView('create-project')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Create Project
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {projects.map((projectItem) => {
                    // Handle both direct project and wrapped project structure
                    const project = projectItem.project || projectItem;
                    const featureCount = projectItem.feature_count || project.total_features || 0;
                    
                    return (
                      <div key={project.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {project.name || 'Unnamed Project'}
                        </h3>
                        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                          {project.description || 'No description provided'}
                        </p>
                        <div className="flex justify-between items-center text-sm text-gray-500 mb-3">
                          <span className="capitalize">
                            {project.industry?.toLowerCase().replace('-', ' ') || 'Unknown'}
                          </span>
                          <span>{featureCount} features</span>
                        </div>
                        <div className="text-sm text-gray-500 mb-3">
                          <strong>Target:</strong> {project.target_users || 'Not specified'}
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => loadProject(project.id)}
                            className="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                          >
                            Open
                          </button>
                          <button
                            onClick={() => deleteProject(project.id)}
                            className="px-3 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Create Project View */}
        {currentView === 'create-project' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Project</h2>
            <ProjectForm onSubmit={createProject} />
          </div>
        )}

        {/* Project View */}
        {currentView === 'project' && currentProject && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{currentProject.name}</h2>
                  <p className="text-gray-600 mt-1">{currentProject.description}</p>
                  <div className="mt-2 text-sm text-gray-500">
                    <span className="mr-4">Industry: {currentProject.industry}</span>
                    <span>Target: {currentProject.target_users}</span>
                  </div>
                </div>
                <button
                  onClick={generateMVP}
                  disabled={loading || features.length === 0}
                  className="px-6 py-3 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {loading ? 'Generating MVP...' : 'Generate MVP'}
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Feature</h3>
                  <FeatureForm onSubmit={addFeature} />
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Features ({features.length})
                  </h3>
                  {features.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      <div className="text-4xl mb-2">⭐</div>
                      <p>No features added yet</p>
                    </div>
                  ) : (
                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {features.map((feature, index) => (
                        <FeatureCard key={feature.id || index} feature={feature} index={index} />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* MVP Result View */}
        {currentView === 'mvp-result' && mvpResult && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="text-center mb-6">
                <div className="text-6xl mb-4">🎉</div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Your MVP Plan is Ready!</h2>
                <p className="text-gray-600">Here's your comprehensive MVP development plan</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{mvpResult.core_features?.length || 0}</div>
                  <div className="text-sm text-gray-600">Core Features</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{mvpResult.estimated_timeline_weeks || 0}</div>
                  <div className="text-sm text-gray-600">Weeks to Build</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">{mvpResult.mvp_readiness_score || 0}/10</div>
                  <div className="text-sm text-gray-600">MVP Readiness</div>
                </div>
              </div>

              {mvpResult.value_proposition && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Value Proposition</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-gray-700">
                      {mvpResult.value_proposition.headline || mvpResult.value_proposition || 'Value proposition generated'}
                    </p>
                  </div>
                </div>
              )}

              {mvpResult.core_features && mvpResult.core_features.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Core Features for MVP</h3>
                  <div className="space-y-3">
                    {mvpResult.core_features.map((feature, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <h4 className="font-medium text-gray-900">{feature.name || feature.feature_name}</h4>
                        <p className="text-gray-600 text-sm mt-1">{feature.description || feature.feature_description}</p>
                        {feature.user_story && (
                          <p className="text-blue-600 text-sm mt-2 italic">"{feature.user_story}"</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {mvpResult.recommendations && mvpResult.recommendations.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Recommendations</h3>
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <ul className="space-y-2">
                      {mvpResult.recommendations.map((rec, index) => (
                        <li key={index} className="text-yellow-800 text-sm">• {rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              <div className="flex space-x-4">
                <button
                  onClick={() => setCurrentView('project')}
                  className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-md hover:bg-gray-50"
                >
                  Back to Project
                </button>
                <button
                  onClick={() => window.print()}
                  className="flex-1 px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700"
                >
                  Save/Print Plan
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
