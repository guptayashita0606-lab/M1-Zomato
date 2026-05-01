# Restaurant Recommendations - Next.js Frontend

Phase 7 implementation of the restaurant recommendation system using Next.js 14 with TypeScript and Tailwind CSS.

## Features

- **Modern Web Interface**: Clean, responsive design using Next.js 14 and Tailwind CSS
- **Preference Form**: Comprehensive form with validation for location, budget, cuisines, and ratings
- **Real-time Recommendations**: AI-powered restaurant suggestions from Phase 6 API
- **Loading States**: Smooth loading indicators and error handling
- **Empty States**: Helpful messages when no restaurants match criteria
- **Copy as Markdown**: Export recommendations in Markdown format
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Architecture

This frontend implements Phase 7 of the milestone architecture:

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom color scheme
- **API Integration**: Axios client with timeout handling
- **State Management**: React hooks (useState, useEffect)
- **Type Safety**: TypeScript throughout
- **Icons**: Lucide React for consistent iconography

## Prerequisites

- Node.js 18+ 
- Phase 6 API server running on `http://localhost:8000`

## Quick Start

### 1. Install Dependencies

```bash
cd frontend-nextjs
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 3. Start Backend API

In a separate terminal, start the Phase 6 API:

```bash
cd ..
python run_api.py
```

The API will be available at `http://localhost:8000`

## Demo Path

1. **Start both servers** (frontend on :3000, backend on :8000)
2. **Open browser** to `http://localhost:3000`
3. **Fill preferences**:
   - Enter a location (e.g., "Delhi")
   - Select budget (low/medium/high)
   - Add cuisines (e.g., "Italian", "Chinese")
   - Set minimum rating (e.g., 4.0)
4. **Click "Get Recommendations"**
5. **View results** with AI explanations
6. **Test empty states** by using restrictive filters

## Project Structure

```
frontend-nextjs/
├── src/
│   ├── app/
│   │   ├── globals.css          # Global styles
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home page
│   ├── components/
│   │   ├── forms/
│   │   │   └── preference-form.tsx    # Preference form component
│   │   ├── recommendations/
│   │   │   ├── recommendation-results.tsx  # Results container
│   │   │   ├── restaurant-card.tsx       # Individual restaurant card
│   │   │   └── empty-state.tsx            # Empty state component
│   │   └── layout/
│   │       ├── header.tsx              # Site header
│   │       └── footer.tsx              # Site footer
│   ├── services/
│   │   └── api.ts                 # API client service
│   └── types/
│       └── api.ts                 # TypeScript type definitions
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

## API Integration

The frontend communicates exclusively with the Phase 6 API:

### Endpoints Used

- `GET /api/v1/meta` - Get available cities and options
- `POST /api/v1/recommendations` - Generate recommendations
- `GET /health` - Check API health status

### Request/Response Flow

1. **Form Submission** → POST `/api/v1/recommendations`
2. **Loading State** → Show spinner during API call
3. **Success Response** → Display restaurant recommendations
4. **Error Handling** → Show user-friendly error messages
5. **Empty Results** → Display helpful suggestions

## UI Components

### PreferenceForm
- Location input with city suggestions
- Budget selection (radio buttons)
- Multi-select cuisine preferences
- Rating slider (1.0-5.0)
- Form validation and error handling

### RestaurantCard
- Restaurant name and rating
- Cuisine type badges
- Price range indicator
- AI explanation
- Copy as Markdown functionality

### EmptyState
- Friendly no-results message
- Helpful suggestions for refining search
- Option to start new search

## Styling

### Color Scheme
- **Primary**: Orange (#f97316) - Main actions and accents
- **Secondary**: Blue (#3b82f6) - Links and secondary elements
- **Neutral**: Gray scale for text and backgrounds
- **Success**: Green for positive feedback
- **Error**: Red for error states

### Responsive Design
- **Mobile**: Single column layout, optimized for touch
- **Tablet**: Two-column grid for restaurant cards
- **Desktop**: Full layout with optimal spacing

## Environment Variables

Create `.env.local` for production:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Build and Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## Exit Criteria Met

✅ **Primary user surface** with preference form + recommendation list  
✅ **Browser communicates only with Phase 6 API**  
✅ **UI contract** shows name, cuisines, rating, estimated cost, AI explanation  
✅ **Empty states** for no filter matches and no grounded model picks  
✅ **UX features**: Loading state, inline validation, disabled submit while pending, copy as Markdown  
✅ **Stack consistency**: Next.js + TypeScript + Tailwind CSS  

## Troubleshooting

### API Connection Issues
- Ensure Phase 6 API is running on `http://localhost:8000`
- Check CORS configuration in backend
- Verify API timeout settings (35 seconds)

### Build Errors
- Run `npm install` to ensure all dependencies
- Check TypeScript configuration
- Verify Tailwind CSS setup

### Styling Issues
- Ensure Tailwind CSS is properly configured
- Check global CSS imports
- Verify responsive breakpoints

## Next Steps

This Phase 7 implementation provides a complete frontend solution that integrates seamlessly with the Phase 6 backend API, offering users a modern, intuitive interface for AI-powered restaurant recommendations.
