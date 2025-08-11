import React from 'react';
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  TrendingUp,
  Zap,
  Users,
  Target,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { useState } from 'react';

const ValidationResult = ({ data }) => {
  const [showDetails, setShowDetails] = useState(false);
  
  if (!data) return null;

  const { feature, result, timestamp, processing_time } = data;

  // Decision styling
  const getDecisionStyle = (decision) => {
    switch (decision) {
      case 'ACCEPT':
        return {
          bg: 'bg-success-50',
          border: 'border-success-200',
          text: 'text-success-800',
          icon: CheckCircle,
          iconColor: 'text-success-600'
        };
      case 'MODIFY':
        return {
          bg: 'bg-warning-50',
          border: 'border-warning-200',
          text: 'text-warning-800',
          icon: AlertTriangle,
          iconColor: 'text-warning-600'
        };
      case 'DEFER':
        return {
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          text: 'text-blue-800',
          icon: Clock,
          iconColor: 'text-blue-600'
        };
      case 'REJECT':
        return {
          bg: 'bg-danger-50',
          border: 'border-danger-200',
          text: 'text-danger-800',
          icon: XCircle,
          iconColor: 'text-danger-600'
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          text: 'text-gray-800',
          icon: AlertTriangle,
          iconColor: 'text-gray-600'
        };
    }
  };

  const decisionStyle = getDecisionStyle(result.decision);
  const DecisionIcon = decisionStyle.icon;

  // Score color based on value
  const getScoreColor = (score) => {
    if (score >= 8) return 'bg-success-500';
    if (score >= 6) return 'bg-warning-500';
    if (score >= 4) return 'bg-orange-500';
    return 'bg-danger-500';
  };

  const ScoreBar = ({ label, score, icon: Icon }) => (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Icon className="h-4 w-4 text-gray-600" />
          <span className="text-sm font-medium text-gray-700">{label}</span>
        </div>
        <span className="text-sm font-bold text-gray-900">{score}/10</span>
      </div>
      <div className="progress-bar">
        <div 
          className={`progress-fill ${getScoreColor(score)}`}
          style={{ width: `${(score / 10) * 100}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Decision Card */}
      <div className={`card ${decisionStyle.bg} ${decisionStyle.border}`}>
        <div className="flex items-start space-x-4">
          <DecisionIcon className={`h-8 w-8 ${decisionStyle.iconColor} flex-shrink-0 mt-1`} />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <h3 className={`text-lg font-bold ${decisionStyle.text}`}>
                {result.decision}
              </h3>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <span>Confidence: {Math.round(result.confidence * 100)}%</span>
              </div>
            </div>
            <p className={`${decisionStyle.text} leading-relaxed`}>
              {result.rationale}
            </p>
          </div>
        </div>
      </div>

      {/* Scores Card */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Analysis Scores</h3>
        <div className="space-y-6">
          <ScoreBar 
            label="MVP Essentiality" 
            score={result.score.core_mvp_score} 
            icon={Target}
          />
          <ScoreBar 
            label="User Value" 
            score={result.score.user_value_score} 
            icon={Users}
          />
          <ScoreBar 
            label="Implementation Complexity" 
            score={result.score.complexity_score} 
            icon={Zap}
          />
          <div className="pt-4 border-t border-gray-200">
            <ScoreBar 
              label="Overall Score" 
              score={result.score.overall_score} 
              icon={TrendingUp}
            />
          </div>
        </div>
      </div>

      {/* Timeline Impact */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Clock className="h-5 w-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">Timeline Impact</h3>
        </div>
        <p className="text-gray-700">{result.timeline_impact}</p>
      </div>

      {/* Alternatives */}
      {result.alternatives && result.alternatives.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Recommended Alternatives
          </h3>
          <div className="space-y-3">
            {result.alternatives.map((alternative, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
                  {index + 1}
                </div>
                <p className="text-gray-700 leading-relaxed">{alternative}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dependencies */}
      {result.dependencies && result.dependencies.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Technical Dependencies
          </h3>
          <div className="space-y-2">
            {result.dependencies.map((dependency, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-primary-500 rounded-full" />
                <span className="text-gray-700">{dependency}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feature Details (Collapsible) */}
      <div className="card">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="w-full flex items-center justify-between text-left"
        >
          <h3 className="text-lg font-semibold text-gray-900">
            Feature Details
          </h3>
          {showDetails ? (
            <ChevronUp className="h-5 w-5 text-gray-500" />
          ) : (
            <ChevronDown className="h-5 w-5 text-gray-500" />
          )}
        </button>
        
        {showDetails && (
          <div className="mt-4 space-y-4 pt-4 border-t border-gray-200">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Feature Name</h4>
              <p className="text-gray-700">{feature.name}</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Description</h4>
              <p className="text-gray-700 leading-relaxed">{feature.description}</p>
            </div>
            
            {feature.user_story && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">User Story</h4>
                <p className="text-gray-700 italic">{feature.user_story}</p>
              </div>
            )}
            
            {feature.acceptance_criteria && feature.acceptance_criteria.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Acceptance Criteria</h4>
                <ul className="space-y-1">
                  {feature.acceptance_criteria.map((criterion, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-primary-500 mt-1">•</span>
                      <span className="text-gray-700">{criterion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-100">
              <span>Priority: {feature.priority}</span>
              <span>Analyzed in {processing_time.toFixed(2)}s</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ValidationResult;
