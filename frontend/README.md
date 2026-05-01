# Frontend - Restaurant Recommendation UI

React + TypeScript frontend for the restaurant recommendation system.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Features

- Location input with city suggestions
- Budget selection (low/medium/high)
- Cuisine preferences with multi-select
- Rating slider
- Real-time recommendation display
- Error handling and loading states
- Responsive design with Tailwind CSS

## API Integration

The frontend communicates with the backend API running on `http://localhost:8000`:
- `GET /health` - Health check
- `GET /api/v1/meta` - Available options
- `POST /api/v1/recommendations` - Generate recommendations

## Build

```bash
npm run build
```

## Preview

```bash
npm run preview
```
