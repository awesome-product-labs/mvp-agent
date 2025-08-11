import React, { useState } from 'react';
import axios from 'axios';

const MVPGenerator = ({ project, features }) => {
  const [mvpDefinition, setMvpDefinition] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');

  const generateMVP = async () => {
    if (!project?.id) return;
    
    setGenerating(true);
    setError('');
    
    try {
      const response = await axios.post(`/api/v1/projects/${project.id}/generate-mvp`, {
        project_id: project.id,
        max_timeline_weeks: 12,
        priority_threshold: 'medium'
      });
      
      setMvpDefinition(response.data);
    } catch (err) {
      console.error('MVP generation error:', err);
      setError(`Failed to generate MVP: ${err.response?.data?.detail || err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const approvedFeatures = features?.filter(f => f.status === 'APPROVED') || [];

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">MVP Generation</h2>
            <p className="text-gray-600 mt-1">
              Generate a complete MVP definition with value proposition for {project?.name}
            </p>
          </div>
          <button
            onClick={generateMVP}
            disabled={generating || approvedFeatures.length === 0}
            className="px-6 py-3 bg-purple-600 text-white font-medium rounded-md hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {generating ? 'Generating MVP...' : 'Generate MVP'}
          </button>
        </div>
        
        {approvedFeatures.length === 0 && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-yellow-800">
              Add and approve some features first to generate an MVP.
            </p>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* MVP Definition */}
      {mvpDefinition && (
        <div className="space-y-6">
          {/* Value Proposition */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">🎯 Value Proposition</h3>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Headline</h4>
                <p className="text-lg text-blue-600 font-medium">
                  {mvpDefinition.value_proposition.headline}
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Problem Statement</h4>
                <p className="text-gray-700">
                  {mvpDefinition.value_proposition.problem_statement}
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Solution Summary</h4>
                <p className="text-gray-700">
                  {mvpDefinition.value_proposition.solution_summary}
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Elevator Pitch</h4>
                <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                  <p className="text-blue-800 italic">
                    "{mvpDefinition.value_proposition.elevator_pitch}"
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Core MVP Features */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">🚀 Core MVP Features</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {mvpDefinition.core_features.map((feature, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-3">
                    <h4 className="font-semibold text-gray-800">{feature.feature_name}</h4>
                    <div className="flex space-x-2">
                      <span className={`px-2 py-1 text-xs rounded ${
                        feature.priority === 'high' ? 'bg-red-100 text-red-800' :
                        feature.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {feature.priority}
                      </span>
                      <span className="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                        {feature.status}
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-3">{feature.feature_description}</p>
                  
                  {feature.user_story && (
                    <div className="bg-blue-50 border-l-4 border-blue-400 p-3 mb-3">
                      <p className="text-sm text-blue-800 italic">"{feature.user_story}"</p>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center text-sm text-gray-500">
                    <span>Effort: {feature.estimated_weeks ? `${feature.estimated_weeks} weeks` : 'TBD'}</span>
                    {feature.validation_result && feature.validation_result.score && (
                      <span>Score: {feature.validation_result.score.overall_score}/10</span>
                    )}
                  </div>
                  
                  {feature.acceptance_criteria && feature.acceptance_criteria.length > 0 && (
                    <div className="mt-3">
                      <h5 className="text-xs font-medium text-gray-500 uppercase mb-1">Acceptance Criteria</h5>
                      <ul className="text-xs text-gray-600 space-y-1">
                        {feature.acceptance_criteria.slice(0, 2).map((criteria, i) => (
                          <li key={i}>• {criteria}</li>
                        ))}
                        {feature.acceptance_criteria.length > 2 && (
                          <li className="text-gray-400">+ {feature.acceptance_criteria.length - 2} more...</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* MVP Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">📊 MVP Overview</h3>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Timeline:</span>
                  <span className="font-medium">{mvpDefinition.estimated_timeline_weeks} weeks</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Effort:</span>
                  <span className="font-medium">{mvpDefinition.estimated_effort_hours} hours</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Core Features:</span>
                  <span className="font-medium">{mvpDefinition.core_features.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Confidence:</span>
                  <span className="font-medium">
                    {Math.round(mvpDefinition.value_proposition.confidence_score * 100)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🎯 Success Metrics</h3>
              
              <ul className="space-y-2">
                {mvpDefinition.success_metrics.slice(0, 5).map((metric, index) => (
                  <li key={index} className="flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                    <span className="text-gray-700">{metric}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* User Personas */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">👥 User Personas</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mvpDefinition.user_personas.map((persona, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-800 mb-2">{persona.name}</h4>
                  <p className="text-gray-600 text-sm mb-3">{persona.description}</p>
                  
                  <div className="space-y-2">
                    <div>
                      <span className="text-xs font-medium text-gray-500 uppercase">Pain Points</span>
                      <ul className="text-sm text-gray-700 mt-1">
                        {persona.pain_points.slice(0, 2).map((point, i) => (
                          <li key={i}>• {point}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div>
                      <span className="text-xs font-medium text-gray-500 uppercase">Goals</span>
                      <ul className="text-sm text-gray-700 mt-1">
                        {persona.goals.slice(0, 2).map((goal, i) => (
                          <li key={i}>• {goal}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* User Benefits */}
          {mvpDefinition.value_proposition.target_user_benefits && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">💡 User Benefits</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mvpDefinition.value_proposition.target_user_benefits.map((benefit, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-800">{benefit.user_type}</h4>
                      <span className={`px-2 py-1 text-xs rounded ${
                        benefit.priority === 'high' ? 'bg-red-100 text-red-800' :
                        benefit.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {benefit.priority}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{benefit.pain_point}</p>
                    <p className="text-sm text-blue-600 font-medium">{benefit.benefit}</p>
                    <p className="text-xs text-gray-500 mt-1">Metric: {benefit.value_metric}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Competitive Analysis */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">🏆 Competitive Analysis</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Direct Competitors</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  {mvpDefinition.competitive_analysis.direct_competitors.map((competitor, index) => (
                    <li key={index}>• {competitor}</li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Market Gaps</h4>
                <ul className="text-sm text-gray-700 space-y-1">
                  {mvpDefinition.competitive_analysis.market_gaps.map((gap, index) => (
                    <li key={index}>• {gap}</li>
                  ))}
                </ul>
              </div>
            </div>
            
            <div className="mt-4">
              <h4 className="font-semibold text-gray-800 mb-2">Competitive Advantages</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mvpDefinition.value_proposition.competitive_advantages.map((advantage, index) => (
                  <div key={index} className="bg-green-50 border border-green-200 rounded-md p-3">
                    <h5 className="font-medium text-green-800">{advantage.advantage}</h5>
                    <p className="text-sm text-green-700 mt-1">{advantage.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Technical Requirements & Risks */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">⚙️ Technical Requirements</h3>
              
              <ul className="space-y-2">
                {mvpDefinition.technical_requirements.map((req, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-3 mt-2"></span>
                    <span className="text-gray-700 text-sm">{req}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">⚠️ Risks & Assumptions</h3>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-800 mb-2">Key Risks</h4>
                  <ul className="space-y-1">
                    {mvpDefinition.risks.slice(0, 3).map((risk, index) => (
                      <li key={index} className="flex items-start">
                        <span className="w-2 h-2 bg-red-500 rounded-full mr-3 mt-2"></span>
                        <span className="text-gray-700 text-sm">{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-800 mb-2">Key Assumptions</h4>
                  <ul className="space-y-1">
                    {mvpDefinition.assumptions.slice(0, 3).map((assumption, index) => (
                      <li key={index} className="flex items-start">
                        <span className="w-2 h-2 bg-yellow-500 rounded-full mr-3 mt-2"></span>
                        <span className="text-gray-700 text-sm">{assumption}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* User Journey */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">🛤️ Target User Journey</h3>
            
            <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
              <p className="text-gray-700">{mvpDefinition.target_user_journey}</p>
            </div>
            
            {mvpDefinition.value_proposition.user_journey_value && (
              <div className="mt-4">
                <h4 className="font-medium text-gray-800 mb-2">Journey Value</h4>
                <p className="text-gray-700">{mvpDefinition.value_proposition.user_journey_value}</p>
              </div>
            )}
          </div>

          {/* Market Positioning */}
          {mvpDefinition.value_proposition.market_positioning && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🎯 Market Positioning</h3>
              
              <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                <p className="text-blue-800">{mvpDefinition.value_proposition.market_positioning}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MVPGenerator;
