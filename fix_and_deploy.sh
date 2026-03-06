#!/bin/bash
set -e

echo "=========================================="
echo "Fixing and Redeploying to Render"
echo "=========================================="
echo ""

echo "✅ Fix applied: render.yaml now uses 'app:app' instead of 'backend.main:app'"
echo ""

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo "Changes to commit:"
    git status --short
    echo ""
    
    # Add and commit
    git add render.yaml start.sh RENDER_FIX.md fix_and_deploy.sh
    git commit -m "Fix: Use app:app in startCommand for Render deployment"
    echo "✅ Changes committed"
else
    echo "✅ No changes to commit"
fi

# Push to GitHub
echo ""
read -p "Push to GitHub and trigger Render redeploy? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to GitHub..."
    git push origin main || git push origin master
    echo ""
    echo "=========================================="
    echo "✅ Pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "Render will automatically detect the changes and redeploy."
    echo ""
    echo "Monitor the deployment at:"
    echo "  https://dashboard.render.com"
    echo ""
    echo "Expected timeline:"
    echo "  • Detection: ~30 seconds"
    echo "  • Build: ~5-10 minutes"
    echo "  • Deploy: ~1 minute"
    echo ""
    echo "Once deployed, test with:"
    echo "  curl https://your-app.onrender.com/"
    echo ""
    echo "=========================================="
else
    echo "⚠️  Push cancelled"
    echo ""
    echo "To deploy later, run:"
    echo "  git push origin main"
fi
