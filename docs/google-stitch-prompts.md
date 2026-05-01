# Google Stitch Prompts for Frontend UI Generation

This document contains prompts for Google Stitch to generate frontend UI images for the Restaurant Recommendation System using Next.js framework.

## Overview

The frontend is a restaurant recommendation web application where users can:
- Input their dining preferences (location, budget, cuisines, rating)
- Receive AI-powered restaurant recommendations
- View restaurant details with explanations

## Google Stitch Prompts

### Main Application Layout

**Prompt 1: Landing Page Layout**
```
Create a modern restaurant recommendation web application landing page using Next.js and Tailwind CSS. The page should have:

Header:
- Logo with restaurant icon
- Navigation menu with "Home", "About", "Contact"
- Clean, modern design with orange accent color

Hero Section:
- Large headline "Discover Amazing Restaurants"
- Subheading "AI-powered recommendations tailored to your taste"
- Call-to-action button "Get Recommendations"
- Background image of elegant restaurant interior

Features Section:
- Three cards showing "Smart Recommendations", "Personalized Results", "Trusted Reviews"
- Icons and brief descriptions for each feature

Footer:
- Copyright information
- Social media links
- Quick links

Use modern design principles, clean typography, and professional restaurant industry aesthetics. Responsive design for mobile and desktop.
```

**Prompt 2: Preference Form Interface**
```
Design a comprehensive restaurant preference form for a Next.js application using Tailwind CSS. The form should include:

Layout:
- Clean, organized form with proper spacing
- Progress indicator showing form steps
- Responsive grid layout

Form Fields:
1. Location Input:
   - Text input with location icon
   - Dropdown suggestions for popular cities
   - "Current location" button with geolocation

2. Budget Selection:
   - Three radio buttons: "Low ($)", "Medium ($$)", "High ($$$)"
   - Visual indicators with dollar signs
   - Clear selection state

3. Cuisine Preferences:
   - Multi-select cuisine tags
   - Searchable dropdown with popular cuisines
   - Selected cuisines shown as removable pills
   - Categories: Italian, Chinese, Indian, Mexican, Japanese, etc.

4. Rating Slider:
   - Interactive range slider from 1.0 to 5.0 stars
   - Visual star indicators
   - Current rating display

5. Additional Preferences:
   - Text area for special requirements
   - Optional dietary restrictions checkboxes

Submit Section:
- Large "Get Recommendations" button
- Loading state with spinner
- Form validation messages

Use modern form design with clear visual hierarchy, proper validation states, and smooth interactions.
```

**Prompt 3: Recommendations Display**
```
Create a restaurant recommendations results page for Next.js with Tailwind CSS. The design should show:

Results Header:
- "Recommended Restaurants" title
- Filter options (sort by rating, price, distance)
- Results count display
- View toggle (grid/list)

Restaurant Cards:
- Clean card design with restaurant image placeholder
- Restaurant name and rating stars
- Cuisine type badges
- Price range indicator ($-$$$)
- Distance from location
- "View Details" button
- "Save to Favorites" heart icon

Card Layout (Grid View):
- Responsive 2-3 column grid
- Consistent card heights
- Hover effects and transitions

Card Layout (List View):
- Horizontal layout with image on left
- Detailed information on right
- More compact design

Empty State:
- Friendly message when no results found
- Suggestions to adjust filters
- "Search Again" button

Loading State:
- Skeleton loaders for restaurant cards
- Smooth animation effects

Use modern card-based design with professional restaurant industry styling, clear typography, and intuitive user interactions.
```

**Prompt 4: Restaurant Detail Modal**
```
Design a detailed restaurant modal/overlay for Next.js using Tailwind CSS. The modal should include:

Modal Layout:
- Full-screen overlay on mobile, centered modal on desktop
- Smooth fade-in animation
- Close button and escape key functionality

Restaurant Header:
- Large restaurant hero image
- Restaurant name with prominent typography
- Overall rating with star display
- Price range and cuisine type

Detailed Information:
- Address with map integration placeholder
- Phone number and website links
- Hours of operation
- "Reserve Table" button

Menu Highlights:
- Popular dishes section
- Price information
- Dietary accommodations

AI Recommendation Section:
- "Why we recommend this restaurant" heading
- Personalized explanation text
- Match score with user preferences

Reviews Section:
- Customer reviews summary
- Individual review cards
- Star ratings and dates
- "Read All Reviews" link

Action Buttons:
- "Get Directions" button
- "Share Restaurant" button
- "Add to Favorites" button

Use rich, detailed design with high-quality image placeholders, comprehensive information architecture, and smooth modal interactions.
```

**Prompt 5: Mobile Responsive Design**
```
Create mobile-responsive designs for the restaurant recommendation app in Next.js with Tailwind CSS. Focus on:

Mobile Navigation:
- Hamburger menu for navigation
- Bottom tab bar for main sections
- Touch-friendly button sizes

Mobile Form:
- Stacked form layout
- Large touch targets
- Mobile keyboard optimization
- Swipeable cuisine selector

Mobile Results:
- Single-column card layout
- Pull-to-refresh functionality
- Infinite scroll loading
- Filter drawer from bottom

Mobile Modals:
- Full-screen overlays
- Swipe-to-close gestures
- Optimized content hierarchy

Mobile Specific Features:
- "Near Me" location detection
- Phone number click-to-call
- Mobile map integration
- Share functionality

Use mobile-first design principles with thumb-friendly interactions, optimized layouts, and native mobile app feel.
```

## Technical Specifications for Google Stitch

### Framework Details
```
Framework: Next.js 14 with App Router
Styling: Tailwind CSS
Icons: Lucide React
State Management: React hooks (useState, useEffect)
HTTP Client: Axios or fetch API
Components: Modular, reusable components
```

### Color Scheme
```
Primary: Orange (#FF6B35)
Secondary: Blue (#004E89)
Background: Light gray (#F8F9FA)
Text: Dark gray (#212529)
White: #FFFFFF
Success: Green (#28A745)
Warning: Yellow (#FFC107)
Error: Red (#DC3545)
```

### Typography
```
Headings: Modern sans-serif (Inter, Poppins)
Body: Clean, readable sans-serif
Font weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
Font sizes: Responsive scaling from mobile to desktop
```

### Design Principles
```
- Clean, modern interface
- High contrast for accessibility
- Consistent spacing (8px grid system)
- Smooth transitions and micro-interactions
- Professional restaurant industry aesthetic
- User-friendly error states
- Loading skeletons for better UX
```

## Component Structure

### Page Components
```
/app
  /page.tsx (Home/Landing)
  /recommendations/page.tsx (Results)
  /restaurant/[id]/page.tsx (Details)
```

### UI Components
```
/components
  /ui (Button, Input, Card, Modal)
  /forms (PreferenceForm, LocationInput)
  /restaurant (RestaurantCard, RestaurantDetails)
  /layout (Header, Footer, Navigation)
```

### Data Flow
```
User Input → Form Validation → API Call → Loading State → Results Display → User Actions
```

## Usage Instructions

1. Copy these prompts into Google Stitch
2. Specify Next.js and Tailwind CSS as the technology stack
3. Generate UI images based on each prompt
4. Use the generated images as design references for implementation
5. Follow the component structure for organized development

## Additional Notes

- All designs should be responsive and work on mobile and desktop
- Include loading states and error handling in designs
- Follow accessibility best practices (ARIA labels, keyboard navigation)
- Use semantic HTML5 elements
- Include proper error states and empty states
- Design should match the backend API structure
- Include proper form validation feedback
