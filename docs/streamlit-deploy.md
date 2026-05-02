# Streamlit Deployment Guide

## Phase 8 - Streamlit Deployment

This guide covers local development and cloud deployment of the Streamlit application for restaurant recommendations.

## Overview

The Streamlit deployment provides a single-process Python deployment path that replicates the CLI/API flow with a user-friendly web interface.

### Features

- 🎯 **Interactive Preferences**: Location, budget, cuisine, and rating filters
- 🤖 **AI-Powered Recommendations**: Real restaurant data from Hugging Face
- 🎨 **Brand Consistency**: Rosy Hearth theme matching Phase 7 design
- ⚡ **Performance**: Caching for fast responses
- 📱 **Responsive**: Works on desktop and mobile devices

## Local Development

### Prerequisites

- Python 3.8 or higher
- Backend API running on `http://localhost:8004`
- Git repository cloned

### Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements-streamlit.txt
   ```

2. **Start Backend API**
   ```bash
   cd /path/to/repo
   python robust_hf_api.py
   ```

3. **Run Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access Application**
   - Open `http://localhost:8501` in your browser
   - The app will connect to the backend API automatically

### Environment Variables

```bash
# Optional: Custom API URL
export API_BASE_URL="http://localhost:8004"

# Optional: For Streamlit Community Cloud
export GROQ_API_KEY="your-groq-api-key"
```

## Cloud Deployment

### Streamlit Community Cloud

1. **Prepare Repository**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Add Streamlit deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the repository and branch
   - Set main file path: `streamlit_app.py`
   - Configure secrets (if needed)

3. **Set Secrets in Streamlit Cloud**
   ```
   API_BASE_URL: http://your-backend-api-url:8004
   GROQ_API_KEY: your-groq-api-key (optional)
   ```

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your app will be available at a `share.streamlit.io` URL

### Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t zomato-ai-streamlit .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 \
     -e API_BASE_URL="http://host.docker.internal:8004" \
     zomato-ai-streamlit
   ```

3. **Docker Compose (Recommended)**
   ```yaml
   version: '3.8'
   services:
     backend:
       build: .
       command: python robust_hf_api.py
       ports:
         - "8004:8004"
       environment:
         - PYTHONPATH=/app/src
     
     frontend:
       build: .
       command: streamlit run streamlit_app.py --server.port=8501
       ports:
         - "8501:8501"
       environment:
         - API_BASE_URL=http://backend:8004
       depends_on:
         - backend
   ```

## Configuration

### Theme Configuration

The app uses the Rosy Hearth theme from Phase 7. Customize in `streamlit.toml`:

```toml
[theme]
primaryColor = "#b7122a"
backgroundColor = "#fcf9f8"
secondaryBackgroundColor = "#ffffff"
textColor = "#1c1c1c"
```

### Performance Optimization

- **Caching**: API responses are cached for 5 minutes
- **Timeouts**: 30-second timeout for API calls
- **Error Handling**: Graceful fallback for connection issues

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure backend API is running on port 8004
   - Check `API_BASE_URL` environment variable
   - Verify network connectivity

2. **Slow Loading**
   - Check backend API performance
   - Consider reducing cache TTL in `app.py`
   - Monitor API response times

3. **Styling Issues**
   - Ensure custom CSS is loading properly
   - Check browser console for CSS errors
   - Verify theme configuration

4. **Deployment Failures**
   - Check all requirements are in `requirements-streamlit.txt`
   - Verify `streamlit_app.py` is in repository root
   - Ensure proper file permissions

### Debug Mode

Enable debug mode for troubleshooting:

```python
# In streamlit_app.py
import streamlit as st
st.set_option('client.showErrorDetails', True)
```

## Architecture

### File Structure

```
├── streamlit_app.py              # Main entry point
├── requirements-streamlit.txt    # Streamlit dependencies
├── streamlit.toml               # Streamlit configuration
├── Dockerfile                   # Docker deployment
└── src/milestone1/phase8_streamlit/
    ├── __init__.py
    ├── app.py                   # Main application logic
    └── theme.py                 # Theme configuration
```

### Data Flow

1. **User Input** → Streamlit widgets
2. **Validation** → Form validation and sanitization
3. **API Call** → Backend recommendation service
4. **Caching** → Response cached for performance
5. **Rendering** → Restaurant cards with styling

## Security Considerations

- **API Keys**: Store in Streamlit secrets, not in code
- **Input Validation**: All user inputs are validated
- **Timeout Protection**: API calls have timeout limits
- **Error Handling**: Sensitive information not exposed

## Performance Monitoring

Monitor key metrics:
- API response times
- Cache hit rates
- User session duration
- Error rates

## Support

For issues:
1. Check the troubleshooting section
2. Review Streamlit logs
3. Verify backend API status
4. Check deployment configuration

---

**Phase 8 Complete**: Streamlit deployment provides an accessible, user-friendly interface for restaurant recommendations with brand consistency and performance optimization.
