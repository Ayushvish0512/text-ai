#!/bin/bash
set -e

echo "=========================================="
echo "Tiny LLM API - Deploy to Production"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git initialized"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "Uncommitted changes detected:"
    git status --short
    echo ""
    read -p "Commit these changes? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
        echo "✅ Changes committed"
    else
        echo "⚠️  Deployment cancelled - commit changes first"
        exit 1
    fi
else
    echo "✅ No uncommitted changes"
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo ""
    echo "No git remote found."
    echo "Please create a GitHub repository and add it as remote:"
    echo ""
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo ""
    exit 1
fi

echo ""
echo "Git remote:"
git remote -v | head -n 1

# Push to GitHub
echo ""
read -p "Push to GitHub? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub..."
    git push origin main || git push origin master
    echo "✅ Pushed to GitHub"
else
    echo "⚠️  Skipped push"
fi

# Deployment instructions
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Go to: https://dashboard.render.com"
echo "2. Click: New + → Web Service"
echo "3. Connect your GitHub repository"
echo "4. Render will detect render.yaml automatically"
echo "5. Click: Create Web Service"
echo "6. Wait 5-10 minutes for build"
echo ""
echo "Your API will be live at:"
echo "  https://tiny-llm-api.onrender.com"
echo ""
echo "Test with:"
echo "  curl https://tiny-llm-api.onrender.com/"
echo ""
echo "=========================================="
echo "Deployment checklist:"
echo "=========================================="
echo ""
echo "✅ Code committed to Git"
echo "✅ Pushed to GitHub"
echo "⏳ Waiting for Render deployment..."
echo ""
echo "Monitor build at:"
echo "  https://dashboard.render.com"
echo ""
echo "=========================================="
