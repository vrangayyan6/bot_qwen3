#!/bin/bash

# Model Validation Test Suite
# This script runs comprehensive tests to prevent frontend/backend model mismatches
# that can cause the 404 model errors we experienced.

set -e

echo "🧪 Running Model Validation Test Suite..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Backend Tests
echo -e "\n${YELLOW}📊 Running Backend Model Validation Tests...${NC}"
cd backend
export PYTHONPATH="$(pwd)/src"

if python -m pytest tests/test_model_validation.py::TestModelValidation -v; then
    echo -e "${GREEN}✅ Backend model validation tests passed!${NC}"
    BACKEND_PASSED=true
else
    echo -e "${RED}❌ Backend model validation tests failed!${NC}"
    BACKEND_PASSED=false
fi

# Frontend Tests
echo -e "\n${YELLOW}🌐 Running Frontend Model Validation Tests...${NC}"
cd ../frontend

if npm run test:run; then
    echo -e "${GREEN}✅ Frontend model validation tests passed!${NC}"
    FRONTEND_PASSED=true
else
    echo -e "${RED}❌ Frontend model validation tests failed!${NC}"
    FRONTEND_PASSED=false
fi

# Summary
echo -e "\n${YELLOW}📋 Test Summary${NC}"
echo "================"

if [ "$BACKEND_PASSED" = true ] && [ "$FRONTEND_PASSED" = true ]; then
    echo -e "${GREEN}🎉 All model validation tests passed!${NC}"
    echo -e "${GREEN}✅ No frontend/backend model mismatches detected${NC}"
    echo -e "${GREEN}✅ All models follow stable naming conventions${NC}"
    echo -e "${GREEN}✅ No deprecated preview models found${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some model validation tests failed!${NC}"

    if [ "$BACKEND_PASSED" = false ]; then
        echo -e "${RED}   - Backend model configuration issues detected${NC}"
    fi

    if [ "$FRONTEND_PASSED" = false ]; then
        echo -e "${RED}   - Frontend model configuration issues detected${NC}"
    fi

    echo -e "\n${YELLOW}💡 What this means:${NC}"
    echo "   - Your models may not work correctly"
    echo "   - Users might see 404 model errors"
    echo "   - Frontend and backend model configs are out of sync"
    echo ""
    echo -e "${YELLOW}🔧 How to fix:${NC}"
    echo "   - Check that frontend model dropdowns use stable model names"
    echo "   - Ensure backend configuration matches frontend options"
    echo "   - Remove any deprecated 'preview-XX-XX' model names"
    echo "   - Use stable names like 'gemini-2.5-flash' instead of preview versions"

    exit 1
fi
