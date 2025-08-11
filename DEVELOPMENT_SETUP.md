# Development Setup Guide

## Current Status ✅

### Environment Setup
- **Git Repository**: Connected to https://github.com/awesome-product-labs/mvp-agent.git
- **Node.js**: v24.5.0 installed via Homebrew
- **npm**: v11.5.1 installed
- **Homebrew**: v4.6.0 installed

### Running Services
- **Frontend**: http://localhost:3001 (Vite dev server)
- **Backend**: http://localhost:8003 (FastAPI server)

### Project Structure
```
mvp-generation-agent/
├── frontend/           # React + Vite frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   └── App.jsx     # Main app component
│   ├── package.json    # Frontend dependencies
│   └── vite.config.js  # Vite configuration
├── backend/            # FastAPI backend
│   ├── src/
│   │   ├── api/        # API routes and models
│   │   ├── agent/      # MVP generation logic
│   │   ├── services/   # Business logic services
│   │   └── utils/      # Utility functions
│   └── requirements.txt # Python dependencies
└── .gitignore         # Git ignore rules
```

## Development Commands

### Frontend
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend
```bash
cd backend
source venv/bin/activate
python ultimate_mvp_server.py  # Start development server
```

### Git Workflow
```bash
git status           # Check repository status
git add .            # Stage changes
git commit -m "msg"  # Commit changes
git push             # Push to remote repository
```

## Next Steps
- Frontend and backend are both running
- Ready for development and feature implementation
- All changes will be tracked in Git version control
