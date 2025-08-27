#!/bin/bash

# 🚀 dbt Course - MkDocs Setup Script
# This script sets up the MkDocs environment for the dbt course

echo "🚀 Setting up MkDocs environment for dbt course..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install MkDocs dependencies
echo "📚 Installing MkDocs dependencies..."
pip install -r requirements-mkdocs.txt

# Verify installation
echo "✅ Verifying installation..."
mkdocs --version

# Build the site
echo "🏗️ Building the site..."
mkdocs build

echo ""
echo "🎉 Setup complete! Your MkDocs environment is ready."
echo ""
echo "📖 Next steps:"
echo "   1. Run 'mkdocs serve' to view the site locally"
echo "   2. Open http://127.0.0.1:8000 in your browser"
echo "   3. Make changes to docs/ files and see live updates"
echo "   4. Commit and push to trigger GitHub Pages deployment"
echo ""
echo "🔗 Useful commands:"
echo "   mkdocs serve          # Start local development server"
echo "   mkdocs build          # Build static site"
echo "   mkdocs gh-deploy      # Deploy to GitHub Pages (if configured)"
echo ""
echo "📚 Documentation: https://www.mkdocs.org/"
echo "🎨 Material theme: https://squidfunk.github.io/mkdocs-material/"

