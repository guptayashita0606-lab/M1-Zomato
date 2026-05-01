# Backend and Frontend Architecture

This document describes the updated architecture after Phase 5, introducing a proper backend API and frontend web UI.

## Architecture Overview

The system has evolved from a CLI-only tool to a full-stack web application:

```
┌─────────────────┐    HTTP API    ┌─────────────────┐    Python Lib    ┌─────────────────┐
│   Frontend      │ ◄────────────► │   Backend API   │ ◄────────────► │ Core Pipeline   │
│  (React SPA)    │                │   (FastAPI)     │                │  (Phases 0-5)   │
└─────────────────┘                └─────────────────┘                └─────────────────┘
     http://localhost:5173          http://localhost:8000
```

## Phase 6 - Backend API

### Responsibilities
- **API Gateway**: Single entry point for all client requests
- **Security**: Manages server-side secrets (GROQ_API_KEY)
- **Orchestration**: Coordinates the core recommendation pipeline
- **Validation**: Input validation and error handling
- **Telemetry**: Request tracking and performance monitoring

### Technology Stack
- **Framework**: FastAPI with async support
- **Validation**: Pydantic models for request/response
- **Server**: Uvicorn ASGI server
- **CORS**: Configured for frontend development

### API Endpoints

#### POST /api/v1/recommendations
**Request**:
```json
{
  "location": "Delhi",
  "budget_band": "medium",
  "cuisines": ["Italian", "Chinese"],
  "minimum_rating": 4.0,
  "top_k": 5,
  "source": "hf"
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "name": "Restaurant Name",
      "cuisines": ["Italian", "Continental"],
      "rating": 4.5,
      "estimated_cost": "₹800 for two",
      "explanation": "Great ambiance and authentic Italian cuisine..."
    }
  ],
  "source": "llm",
  "total_candidates": 150,
  "filtered_candidates": 12,
  "request_id": "uuid-string",
  "telemetry": {...}
}
```

#### GET /health
Health check with dependency status.

#### GET /api/v1/meta
Returns available options for frontend forms:
- Allowed cities from dataset
- Supported budget bands
- Popular cuisines
- Rating ranges

### Implementation Details

**Service Layer** (`service.py`):
- `RecommendationService` class encapsulates business logic
- Caches allowed cities for performance
- Handles errors gracefully with fallback responses

**Models** (`models.py`):
- Pydantic models ensure type safety
- Automatic validation and serialization
- Clear API contract documentation

**Application** (`app.py`):
- FastAPI app factory pattern
- CORS middleware for development
- Global exception handlers
- Lifecycle management

## Phase 7 - Frontend Web UI

### Responsibilities
- **User Interface**: Modern, responsive web interface
- **Form Handling**: Preference input with validation
- **API Integration**: Communicates with backend API only
- **User Experience**: Loading states, error handling, empty states
- **Display**: Restaurant recommendations with explanations

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS for utility-first styling
- **Icons**: Lucide React for consistent iconography
- **HTTP Client**: Axios for API calls

### Component Architecture

**App.tsx** (Main Component):
- State management for preferences and recommendations
- API integration with error handling
- Form submission and loading states
- Recommendation rendering

**Key Features**:
- Location input with city suggestions
- Budget band selection (radio buttons)
- Multi-select cuisine preferences
- Rating slider (1.0-5.0)
- Real-time validation feedback
- Loading spinner during API calls
- Error display with actionable messages
- Restaurant cards with ratings and explanations

### UI/UX Design

**Design Principles**:
- Clean, modern interface with orange accent color
- Mobile-responsive layout
- Clear visual hierarchy
- Accessible form controls
- Consistent spacing and typography

**User Flow**:
1. User enters location and preferences
2. Real-time validation provides feedback
3. Submit triggers API call with loading state
4. Recommendations displayed in card format
5. Empty states handled gracefully

**Error Handling**:
- Network errors with retry suggestions
- Validation errors with field-specific feedback
- Empty result sets with helpful messages
- API errors with user-friendly explanations

## Development Workflow

### Backend Development
```bash
# Install dependencies
pip install -e ".[api,llm,ingestion,dev]"

# Run API server
python run_api.py

# API docs at http://localhost:8000/docs
```

### Frontend Development
```bash
# Install dependencies
cd frontend && npm install

# Run dev server
npm run dev

# App at http://localhost:5173
```

### Production Considerations

**Backend**:
- Use production WSGI server (Gunicorn/Uvicorn)
- Environment-based configuration
- API rate limiting and authentication
- Logging and monitoring

**Frontend**:
- Build optimization: `npm run build`
- Static asset serving
- Environment-specific API URLs
- Browser caching strategies

## Security Architecture

**API Security**:
- Server-side secret management
- Request validation and sanitization
- CORS policy for production domains
- Rate limiting and abuse prevention

**Frontend Security**:
- No API keys exposed to client
- Input validation on both client and server
- XSS protection through React
- Secure HTTP headers

## Performance Optimization

**Backend Optimizations**:
- Async request handling
- City caching in service layer
- Efficient data loading from Hugging Face
- Request timeout management

**Frontend Optimizations**:
- Vite's fast hot reload
- Code splitting for production
- Optimistic UI updates
- Debounced form inputs

## Future Enhancements

**Backend**:
- Database caching for restaurants
- API authentication and user accounts
- Request deduplication
- Advanced analytics and telemetry

**Frontend**:
- Map integration for location selection
- Restaurant detail pages
- User preference persistence
- Advanced filtering and sorting

## Migration Path

The CLI interface remains available for development and testing, ensuring backward compatibility while providing a modern web interface for end users.
