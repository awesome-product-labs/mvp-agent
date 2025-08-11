# MVP Generation Agent

An AI-powered system that helps validate and generate MVPs by analyzing feature requests and providing intelligent recommendations.

## Features

- **Feature Validation**: Uses Claude AI to analyze feature requests for MVP suitability
- **Intelligent Scoring**: Evaluates features on complexity, user value, and MVP fit
- **Smart Recommendations**: Provides alternatives and modifications for complex features
- **Real-time Analysis**: Interactive web interface for immediate feedback

## Project Structure

```
mvp-generation-agent/
├── backend/          # FastAPI backend with Claude integration
├── frontend/         # React frontend with Vite and Tailwind
└── README.md
```

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `ANTHROPIC_API_KEY`: Your Claude API key
- `CORS_ORIGINS`: Allowed CORS origins for development

## Usage

1. Start the backend server on `http://localhost:8000`
2. Start the frontend development server on `http://localhost:3000`
3. Submit feature requests through the web interface
4. Review validation results and recommendations
