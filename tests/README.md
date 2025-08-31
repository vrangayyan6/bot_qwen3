# Test Suite

This directory contains project-wide tests and testing utilities.

## Model Validation Tests

### Purpose
Prevent frontend/backend model mismatches that can cause 404 model errors and application crashes.

### Running Tests
```bash
# Run all model validation tests
./tests/test-model-validation.sh

# Run backend tests only
cd backend && python -m pytest tests/test_model_validation.py -v

# Run frontend tests only
cd frontend && npm run test:run
```

### What is Tested
- ✅ Backend models follow stable naming conventions
- ✅ Frontend model options are valid Gemini models
- ✅ No deprecated preview models in frontend
- ✅ Model names are consistent between frontend and backend
- ✅ Recommended models are stable versions
- ✅ Error dialog fallback models are stable

### Test Structure
- **Backend tests**: `backend/tests/test_model_validation.py`
- **Frontend tests**: `frontend/src/test/model-validation.test.tsx`
- **Integration script**: `tests/test-model-validation.sh`

## Adding New Tests

When adding new models or changing model configurations:

1. Update the regex patterns in both test files to include new model variants
2. Ensure new models follow the `gemini-X.Y-(flash|pro)(-lite)?` naming pattern
3. Test that error handling works with new models
4. Run the full test suite to verify compatibility

## CI Integration

This test suite should be run in CI/CD pipelines to catch model configuration issues before deployment.
