# GitHub Actions Deployment Guide

## Overview

This document explains how to set up automated deployment of your Streamlit app using GitHub Actions.

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Streamlit Cloud Account**: You need a Streamlit Community Cloud account
3. **GitHub Personal Access Token**: For deployment authentication

## Setup Instructions

### 1. Configure Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app" or connect your existing app
3. Select your GitHub repository: `guptayashita0606-lab/M1-Zomato`
4. Set **Main file path** to `app.py` (NOT `streamlit_app.py`)
5. Click "Deploy"

### 2. Set Up GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

#### Required Secrets

- **STREAMLIT_DEPLOY_TOKEN**: Your Streamlit deployment token (optional for basic setup)

### 3. How the Pipeline Works

The GitHub Actions workflow (`.github/workflows/deploy-streamlit.yml`) will:

#### Test Job (Always Runs)
- ✅ Checks out your repository
- ✅ Sets up Python 3.11
- ✅ Installs dependencies from `requirements.txt`
- ✅ Validates Python syntax
- ✅ Tests Streamlit app startup

#### Deploy Job (Main Branch Only)
- ✅ Runs only on successful test completion
- ✅ Deploys to Streamlit Community Cloud
- ✅ Creates deployment configuration
- ✅ Provides deployment status notifications

### 4. Triggers

The pipeline automatically triggers on:
- ✅ **Push to main branch** (with changes to app.py, requirements.txt, or workflows)
- ✅ **Pull requests to main branch** (testing only)
- ✅ **Manual workflow dispatch** (from GitHub Actions tab)

### 5. Deployment URLs

Once deployed, your app will be available at:
- **Primary URL**: https://share.streamlit.io/guptayashita0606-lab/m1-zomato/main
- **Alternative**: https://guptayashita0606-lab-m1-zomato-main-app.streamlit.app/

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're using `app.py` as the main file
2. **Missing Dependencies**: Check `requirements.txt` includes all needed packages
3. **Deployment Failures**: Check GitHub Actions logs for detailed error messages

### Debugging

1. **Local Testing**: Run `streamlit run app.py` locally first
2. **GitHub Actions Logs**: Check the Actions tab in your GitHub repository
3. **Streamlit Cloud Logs**: Check the Streamlit Cloud dashboard for deployment logs

## File Structure

```
Milestone1 zomato/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── .github/workflows/
│   └── deploy-streamlit.yml       # GitHub Actions workflow
├── .streamlit/
│   └── config.toml                # Streamlit configuration
└── docs/
    └── github-actions-deployment.md  # This guide
```

## Best Practices

1. **Always test locally** before pushing changes
2. **Use semantic versioning** for releases
3. **Monitor deployment logs** regularly
4. **Keep dependencies updated** in requirements.txt
5. **Use environment variables** for sensitive data

## Support

If you encounter issues:
1. Check GitHub Actions logs
2. Verify Streamlit Cloud configuration
3. Test the app locally
4. Review the workflow file for syntax errors

## Next Steps

1. ✅ Push your code to GitHub
2. ✅ Set up Streamlit Cloud app with `app.py`
3. ✅ Configure GitHub secrets (if needed)
4. ✅ Test the deployment pipeline
5. ✅ Monitor your automated deployments

Your Streamlit app will now automatically deploy whenever you push changes to the main branch!
