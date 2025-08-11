import React, { useState } from 'react';
import axios from 'axios';

const URLTester = () => {
  const [url, setUrl] = useState('https://github.com');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const testUrl = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      console.log('Testing URL:', url);
      console.log('Making request to:', '/api/v1/analyze-url');
      
      const response = await axios.post('/api/v1/analyze-url', {
        url: url
      });
      
      console.log('Response:', response.data);
      setResult(response.data);
    } catch (err) {
      console.error('Error:', err);
      console.error('Error response:', err.response);
      setError(`Error: ${err.message} - ${err.response?.data?.detail || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const testHealth = async () => {
    try {
      const response = await axios.get('/api/v1/health');
      console.log('Health check:', response.data);
      alert(`Health check successful: ${response.data.status}`);
    } catch (err) {
      console.error('Health check failed:', err);
      alert(`Health check failed: ${err.message}`);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">URL Analysis Tester</h2>
      
      <div className="space-y-4">
        <button
          onClick={testHealth}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Test Health Endpoint
        </button>

        <div>
          <label className="block text-sm font-medium mb-2">Test URL:</label>
          <div className="flex gap-2">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded"
              placeholder="https://example.com"
            />
            <button
              onClick={testUrl}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Testing...' : 'Test URL'}
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {result && (
          <div className="p-4 bg-green-50 border border-green-200 rounded">
            <h3 className="font-semibold mb-2">Analysis Result:</h3>
            <pre className="text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default URLTester;
