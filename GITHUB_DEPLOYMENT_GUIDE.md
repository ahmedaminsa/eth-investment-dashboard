# GitHub Deployment Guide for ETH Investment Dashboard

This guide will walk you through the process of uploading your ETH investment dashboard to GitHub and setting up automatic deployment to Google Cloud App Engine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Creating a GitHub Repository](#creating-a-github-repository)
3. [Setting Up Your Local Environment](#setting-up-your-local-environment)
4. [Uploading Your Code to GitHub](#uploading-your-code-to-github)
5. [Setting Up Continuous Deployment](#setting-up-continuous-deployment)
6. [Making Changes and Updates](#making-changes-and-updates)
7. [Collaborating with Others](#collaborating-with-others)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

1. A GitHub account (sign up at [github.com](https://github.com) if you don't have one)
2. A Google Cloud account with your ETH investment project created
3. Google Cloud Shell access (or Git installed on your local machine)

## Creating a GitHub Repository

1. Go to [github.com](https://github.com) and sign in to your account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Fill in the repository details:
   - Name: `eth-investment-dashboard`
   - Description: `ETH investment dashboard with technical analysis and automated recommendations`
   - Visibility: Choose either "Public" or "Private"
   - Do NOT initialize with README, .gitignore, or license (we'll push your existing code)
4. Click "Create repository"
5. You'll be taken to the repository page with instructions for pushing existing code

## Setting Up Your Local Environment

### Option 1: Using Google Cloud Shell (Recommended)

1. Open Google Cloud Console at [console.cloud.google.com](https://console.cloud.google.com)
2. Make sure your ETH investment project is selected
3. Click the Cloud Shell icon (>_) in the top-right corner
4. Cloud Shell will open at the bottom of the screen
5. Configure Git in Cloud Shell:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### Option 2: Using Your Local Machine

1. Install Git from [git-scm.com](https://git-scm.com/downloads)
2. Open a terminal or command prompt
3. Configure Git:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Uploading Your Code to GitHub

### If You've Already Created Your Dashboard Files

1. Navigate to your project directory:
   ```bash
   # In Cloud Shell
   cd eth-dashboard
   
   # Or on your local machine
   cd path/to/eth-dashboard
   ```

2. Initialize Git repository:
   ```bash
   git init
   ```

3. Add all files to staging:
   ```bash
   git add .
   ```

4. Commit your files:
   ```bash
   git commit -m "Initial commit of ETH investment dashboard"
   ```

5. Connect to your GitHub repository:
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/eth-investment-dashboard.git
   ```
   Replace `YOUR-USERNAME` with your actual GitHub username.

6. Push your code to GitHub:
   ```bash
   git branch -M main
   git push -u origin main
   ```

7. When prompted, enter your GitHub credentials:
   - Username: Your GitHub username
   - Password: Use a personal access token (see below)

### Creating a Personal Access Token

GitHub requires a personal access token for authentication when using HTTPS:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "ETH Dashboard Deployment"
4. Select the "repo" scope to allow full access to repositories
5. Click "Generate token"
6. Copy the token immediately (you won't be able to see it again)
7. Use this token as your password when pushing to GitHub

### If You Haven't Created Your Dashboard Files Yet

1. Clone the empty repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/eth-investment-dashboard.git
   cd eth-investment-dashboard
   ```

2. Create your project structure:
   ```bash
   mkdir -p app_engine/static/css app_engine/static/js app_engine/templates
   ```

3. Create all the necessary files as outlined in the Cloud-Only Deployment Guide

4. Add, commit, and push your files:
   ```bash
   git add .
   git commit -m "Initial commit of ETH investment dashboard"
   git push
   ```

## Setting Up Continuous Deployment

You can set up automatic deployment to Google Cloud App Engine whenever you push changes to GitHub:

### Setting Up Cloud Build

1. In Google Cloud Console, go to Cloud Build → Triggers
2. Click "Create Trigger"
3. Connect to your GitHub repository (you may need to authorize Google Cloud Build)
4. Configure the trigger:
   - Name: `eth-dashboard-deploy`
   - Event: `Push to a branch`
   - Source: `^main$` (regex for main branch)
   - Configuration: `Cloud Build configuration file (yaml or json)`
   - Location: `Repository`
   - Cloud Build configuration file location: `cloudbuild.yaml`
5. Click "Create"

### Creating the Cloud Build Configuration File

Create a file named `cloudbuild.yaml` in your repository:

```yaml
steps:
  # Install dependencies
  - name: 'gcr.io/cloud-builders/npm'
    args: ['install']
    dir: 'app_engine'
  
  # Deploy to App Engine
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['app', 'deploy', '--project=$PROJECT_ID']
    dir: 'app_engine'
```

Add, commit, and push this file:

```bash
git add cloudbuild.yaml
git commit -m "Add Cloud Build configuration"
git push
```

## Making Changes and Updates

After your initial setup, you can make changes to your dashboard and deploy them using Git:

1. Make changes to your files
2. Stage the changes:
   ```bash
   git add .
   ```
3. Commit the changes:
   ```bash
   git commit -m "Description of your changes"
   ```
4. Push to GitHub:
   ```bash
   git push
   ```
5. If you've set up continuous deployment, your changes will automatically deploy to App Engine

## Collaborating with Others

GitHub makes it easy to collaborate with others on your ETH investment dashboard:

### Adding Collaborators

1. Go to your repository on GitHub
2. Click "Settings" → "Collaborators"
3. Click "Add people" and enter their GitHub username or email
4. They'll receive an invitation to collaborate

### Working with Branches

For collaborative development, use branches:

1. Create a new branch for a feature:
   ```bash
   git checkout -b new-feature
   ```
2. Make changes and commit them
3. Push the branch to GitHub:
   ```bash
   git push -u origin new-feature
   ```
4. Create a Pull Request on GitHub to merge changes into the main branch

## Troubleshooting

### Authentication Issues

If you're having trouble authenticating with GitHub:

1. Ensure you're using a personal access token, not your GitHub password
2. Check that your token has the "repo" scope
3. If your token isn't working, generate a new one

### Push Rejected

If your push is rejected:

1. Pull the latest changes:
   ```bash
   git pull --rebase origin main
   ```
2. Resolve any conflicts
3. Try pushing again

### Deployment Failures

If automatic deployment fails:

1. Check the Cloud Build logs in Google Cloud Console
2. Ensure your `cloudbuild.yaml` file is correctly formatted
3. Verify that your App Engine configuration is valid

## Conclusion

By hosting your ETH investment dashboard on GitHub, you gain:

1. **Version Control**: Track all changes to your code
2. **Backup**: Your code is safely stored in GitHub's servers
3. **Collaboration**: Easily work with others on your dashboard
4. **Continuous Deployment**: Automatically deploy changes to Google Cloud
5. **Documentation**: Use GitHub's wiki and README features to document your project

Your ETH investment dashboard is now professionally managed with industry-standard tools and practices!
