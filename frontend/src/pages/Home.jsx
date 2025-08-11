import React from 'react';
import { Zap, Target, Users, TrendingUp, ArrowRight } from 'lucide-react';
import FeatureValidator from '../components/FeatureValidator';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">
                MVP Generation Agent
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              AI-Powered Feature Validation
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Build Better MVPs with{' '}
              <span className="text-gradient">AI-Powered Validation</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Stop building features that don't matter. Get instant AI analysis on feature 
              suitability, complexity, and user value. Make data-driven decisions for your MVP.
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            <div className="card text-center hover:shadow-glow transition-shadow duration-300">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Target className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                MVP Focus
              </h3>
              <p className="text-gray-600 text-sm">
                Analyze features for MVP essentiality and core user value
              </p>
            </div>

            <div className="card text-center hover:shadow-glow transition-shadow duration-300">
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Zap className="h-6 w-6 text-success-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Complexity Analysis
              </h3>
              <p className="text-gray-600 text-sm">
                Get accurate complexity scores and implementation estimates
              </p>
            </div>

            <div className="card text-center hover:shadow-glow transition-shadow duration-300">
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Users className="h-6 w-6 text-warning-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                User Value
              </h3>
              <p className="text-gray-600 text-sm">
                Measure real user impact and prioritize high-value features
              </p>
            </div>

            <div className="card text-center hover:shadow-glow transition-shadow duration-300">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Smart Alternatives
              </h3>
              <p className="text-gray-600 text-sm">
                Get intelligent suggestions for simpler implementations
              </p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium shadow-lg hover:bg-primary-700 transition-colors duration-200">
              <span>Start Validating Features</span>
              <ArrowRight className="h-4 w-4" />
            </div>
          </div>
        </div>
      </section>

      {/* Main Feature Validator */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <FeatureValidator />
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Our AI-powered system analyzes your feature requests using advanced 
              natural language processing and MVP best practices.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Submit Feature
              </h3>
              <p className="text-gray-600">
                Describe your feature idea with as much detail as possible. 
                Include user stories and acceptance criteria for better analysis.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary-600">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                AI Analysis
              </h3>
              <p className="text-gray-600">
                Claude AI analyzes your feature against MVP principles, 
                scoring complexity, user value, and implementation requirements.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary-600">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Get Recommendations
              </h3>
              <p className="text-gray-600">
                Receive detailed analysis with accept/modify/defer/reject decisions, 
                plus alternatives and implementation guidance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-xl font-bold">MVP Generation Agent</h3>
            </div>
            <p className="text-gray-400 mb-6">
              AI-powered feature validation for better MVPs
            </p>
            <div className="text-sm text-gray-500">
              Built with Claude AI, FastAPI, and React
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
