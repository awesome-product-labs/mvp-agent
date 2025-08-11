import React, { useState } from 'react';
import axios from 'axios';

const ProjectCreator = ({ onProjectCreated }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    industry: 'OTHER',
    target_users: '',
    reference_url: '',
    timeline_weeks: '',
    budget_range: '',
    team_size: '',
    team_experience: 'intermediate',
    tech_stack: {
      frontend: [],
      backend: [],
      database: [],
      cloud: [],
      integrations: []
    },
    project_goals: []
  });
  
  const [loading, setLoading] = useState(false);
  const [urlAnalysis, setUrlAnalysis] = useState(null);
  const [analyzingUrl, setAnalyzingUrl] = useState(false);
  const [error, setError] = useState('');

  const industries = [
    { value: 'E-COMMERCE', label: 'E-Commerce' },
    { value: 'FINTECH', label: 'FinTech' },
    { value: 'HEALTHCARE', label: 'Healthcare' },
    { value: 'EDUCATION', label: 'Education' },
    { value: 'SOCIAL', label: 'Social Media' },
    { value: 'PRODUCTIVITY', label: 'Productivity' },
    { value: 'ENTERTAINMENT', label: 'Entertainment' },
    { value: 'OTHER', label: 'Other' }
  ];

  const techStackOptions = {
    frontend: ['React', 'Vue.js', 'Angular', 'Svelte', 'Vanilla JavaScript'],
    backend: ['Node.js', 'Python/Django', 'Python/FastAPI', 'Ruby on Rails', 'ASP.NET Core', 'PHP/Laravel'],
    database: ['PostgreSQL', 'MongoDB', 'MySQL', 'Firebase', 'SQLite'],
    cloud: ['AWS', 'Azure', 'Google Cloud', 'Vercel', 'Netlify', 'Heroku'],
    integrations: ['Stripe', 'Auth0', 'SendGrid', 'Twilio']
  };

  const teamExperienceOptions = [
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' },
    { value: 'expert', label: 'Expert' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const analyzeUrl = async () => {
    if (!formData.reference_url) return;
    
    setAnalyzingUrl(true);
    setError('');
    
    try {
      console.log('Analyzing URL:', formData.reference_url);
      const response = await axios.post('/api/v1/analyze-url', {
        url: formData.reference_url
      });
      
      console.log('URL analysis response:', response.data);
      setUrlAnalysis(response.data);
    } catch (err) {
      console.error('URL analysis error:', err);
      console.error('Error response:', err.response?.data);
      setError(`Failed to analyze URL: ${err.response?.data?.detail || err.message}`);
    } finally {
      setAnalyzingUrl(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Prepare project data
      const projectData = {
        name: formData.name,
        description: formData.description,
        industry: formData.industry,
        target_users: formData.target_users,
        team_experience: formData.team_experience,
        tech_stack: formData.tech_stack,
        ...(formData.reference_url && { reference_url: formData.reference_url }),
        ...(formData.timeline_weeks && { timeline_weeks: parseInt(formData.timeline_weeks) }),
        ...(formData.budget_range && { budget_range: formData.budget_range }),
        ...(formData.team_size && { team_size: parseInt(formData.team_size) }),
        ...(formData.project_goals.length > 0 && { project_goals: formData.project_goals })
      };

      const response = await axios.post('/api/v1/projects', projectData);
      
      if (onProjectCreated) {
        onProjectCreated(response.data);
      }
      
      // Reset form
      setFormData({
        name: '',
        description: '',
        industry: 'OTHER',
        target_users: '',
        reference_url: '',
        timeline_weeks: '',
        budget_range: '',
        team_size: ''
      });
      setUrlAnalysis(null);
      
    } catch (err) {
      setError('Failed to create project. Please try again.');
      console.error('Project creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New MVP Project</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Project Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Project Name *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., TaskFlow MVP"
            />
          </div>

          {/* Industry */}
          <div>
            <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
              Industry *
            </label>
            <select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {industries.map(industry => (
                <option key={industry.value} value={industry.value}>
                  {industry.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Project Description *
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            required
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your MVP project and its main goals..."
          />
        </div>

        {/* Target Users */}
        <div>
          <label htmlFor="target_users" className="block text-sm font-medium text-gray-700 mb-2">
            Target Users *
          </label>
          <textarea
            id="target_users"
            name="target_users"
            value={formData.target_users}
            onChange={handleInputChange}
            required
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe your target audience..."
          />
        </div>

        {/* Reference URL */}
        <div>
          <label htmlFor="reference_url" className="block text-sm font-medium text-gray-700 mb-2">
            Reference URL (Optional)
          </label>
          <div className="flex gap-2">
            <input
              type="url"
              id="reference_url"
              name="reference_url"
              value={formData.reference_url}
              onChange={handleInputChange}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://example.com"
            />
            <button
              type="button"
              onClick={analyzeUrl}
              disabled={!formData.reference_url || analyzingUrl}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {analyzingUrl ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Provide a reference website to analyze existing features and get contextual insights
          </p>
        </div>

        {/* URL Analysis Results */}
        {urlAnalysis && (
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">URL Analysis Results</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium text-blue-800 mb-2">Business Model</h4>
                <p className="text-blue-700 capitalize">{urlAnalysis.context.business_model}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-blue-800 mb-2">Target Audience</h4>
                <p className="text-blue-700">{urlAnalysis.context.target_audience}</p>
              </div>
              
              {urlAnalysis.context.tech_stack.length > 0 && (
                <div>
                  <h4 className="font-medium text-blue-800 mb-2">Tech Stack</h4>
                  <div className="flex flex-wrap gap-1">
                    {urlAnalysis.context.tech_stack.map((tech, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-200 text-blue-800 text-xs rounded">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {urlAnalysis.context.extracted_features.length > 0 && (
                <div>
                  <h4 className="font-medium text-blue-800 mb-2">Key Features</h4>
                  <ul className="text-blue-700 text-sm space-y-1">
                    {urlAnalysis.context.extracted_features.slice(0, 3).map((feature, index) => (
                      <li key={index}>• {feature}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            
            {urlAnalysis.recommendations.length > 0 && (
              <div className="mt-4">
                <h4 className="font-medium text-blue-800 mb-2">Recommendations</h4>
                <ul className="text-blue-700 text-sm space-y-1">
                  {urlAnalysis.recommendations.map((rec, index) => (
                    <li key={index}>• {rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Tech Stack Selection */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tech Stack (Optional)</h3>
          <p className="text-sm text-gray-600 mb-4">Select your preferred technologies for more accurate effort estimation</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(techStackOptions).map(([category, options]) => (
              <div key={category}>
                <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
                  {category}
                </label>
                <div className="space-y-2">
                  {options.map(option => (
                    <label key={option} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={formData.tech_stack[category].includes(option)}
                        onChange={(e) => {
                          const isChecked = e.target.checked;
                          setFormData(prev => ({
                            ...prev,
                            tech_stack: {
                              ...prev.tech_stack,
                              [category]: isChecked
                                ? [...prev.tech_stack[category], option]
                                : prev.tech_stack[category].filter(item => item !== option)
                            }
                          }));
                        }}
                        className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="text-sm text-gray-700">{option}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Team Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="team_size" className="block text-sm font-medium text-gray-700 mb-2">
              Team Size
            </label>
            <input
              type="number"
              id="team_size"
              name="team_size"
              value={formData.team_size}
              onChange={handleInputChange}
              min="1"
              max="50"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="4"
            />
          </div>

          <div>
            <label htmlFor="team_experience" className="block text-sm font-medium text-gray-700 mb-2">
              Team Experience Level
            </label>
            <select
              id="team_experience"
              name="team_experience"
              value={formData.team_experience}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {teamExperienceOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <p className="text-sm text-gray-500 mt-1">
              Affects effort estimation: Expert teams get 50% reduction, beginners get 80% increase
            </p>
          </div>
        </div>

        {/* Additional Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="timeline_weeks" className="block text-sm font-medium text-gray-700 mb-2">
              Timeline (weeks)
            </label>
            <input
              type="number"
              id="timeline_weeks"
              name="timeline_weeks"
              value={formData.timeline_weeks}
              onChange={handleInputChange}
              min="1"
              max="104"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="12"
            />
          </div>

          <div>
            <label htmlFor="budget_range" className="block text-sm font-medium text-gray-700 mb-2">
              Budget Range
            </label>
            <select
              id="budget_range"
              name="budget_range"
              value={formData.budget_range}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select budget range</option>
              <option value="Under $10k">Under $10k</option>
              <option value="$10k - $50k">$10k - $50k</option>
              <option value="$50k - $100k">$50k - $100k</option>
              <option value="$100k - $500k">$100k - $500k</option>
              <option value="Over $500k">Over $500k</option>
            </select>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating Project...' : 'Create Project'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProjectCreator;
