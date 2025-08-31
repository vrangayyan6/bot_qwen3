#!/bin/bash

# Setup pre-commit hooks for the Gemini LangGraph Quickstart project

set -e

echo "🔧 Setting up pre-commit hooks..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit already installed"
fi

# Install frontend dependencies (needed for prettier)
echo "📦 Installing frontend dependencies..."
cd frontend && npm install && cd ..

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Run hooks on all files to verify setup
echo "🧪 Testing hooks on all files..."
pre-commit run --all-files

echo "✅ Pre-commit setup complete!"
echo ""
echo "Pre-commit hooks will now run automatically before each commit."
echo "To run manually: pre-commit run --all-files"
echo "To skip hooks (emergency only): git commit --no-verify"
