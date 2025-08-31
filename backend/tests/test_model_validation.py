"""
Regression tests to validate model configurations and prevent frontend/backend mismatches.

These tests ensure that:
1. Backend default models are valid and available
2. Frontend model options match backend capabilities
3. Model names don't get out of sync between components
"""

import re
from pathlib import Path

import pytest

# Import backend configuration
from agent.configuration import Configuration


def get_frontend_model_names():
    """Extract model names from frontend InputForm.tsx"""
    frontend_path = (
        Path(__file__).parent.parent.parent
        / "frontend"
        / "src"
        / "components"
        / "InputForm.tsx"
    )

    if not frontend_path.exists():
        pytest.skip("Frontend InputForm.tsx not found")

    content = frontend_path.read_text()

    # Extract model names from SelectItem value attributes
    model_pattern = r'value="(gemini-[^"]+)"'
    models = re.findall(model_pattern, content)

    return models


def get_backend_default_models():
    """Get default model names from backend configuration"""
    config = Configuration()
    return {
        "query_generator_model": config.query_generator_model,
        "reflection_model": config.reflection_model,
        "answer_model": config.answer_model,
    }


class TestModelValidation:
    """Test suite for model configuration validation"""

    def test_backend_models_follow_naming_convention(self):
        """Ensure backend models follow Google's stable naming convention"""
        config = Configuration()
        models = [
            config.query_generator_model,
            config.reflection_model,
            config.answer_model,
        ]

        for model in models:
            # Should not contain "preview" (unstable) or specific dates (deprecated)
            assert "preview" not in model, (
                f"Model {model} appears to be a preview/unstable version"
            )
            assert not re.search(r"\d{2}-\d{2}", model), (
                f"Model {model} contains date pattern (likely deprecated)"
            )

            # Should follow gemini-X.Y-model pattern
            assert re.match(r"^gemini-\d+\.\d+-(flash|pro)(-lite)?$", model), (
                f"Model {model} doesn't follow expected naming pattern"
            )

    def test_frontend_models_are_valid_gemini_models(self):
        """Ensure all frontend model options are valid Gemini models"""
        frontend_models = get_frontend_model_names()

        # All models should be valid Gemini models following the naming convention
        for frontend_model in frontend_models:
            assert frontend_model.startswith("gemini-"), (
                f"Model '{frontend_model}' is not a Gemini model"
            )
            assert re.match(r"^gemini-\d+\.\d+-(flash|pro)(-lite)?$", frontend_model), (
                f"Model '{frontend_model}' doesn't follow expected naming pattern"
            )

    def test_no_deprecated_preview_models_in_frontend(self):
        """Ensure frontend doesn't offer deprecated preview models"""
        frontend_models = get_frontend_model_names()

        for model in frontend_models:
            # Flag common deprecated patterns
            assert "preview-04-17" not in model, (
                f"Deprecated model {model} found in frontend"
            )
            assert "preview-05-06" not in model, (
                f"Deprecated model {model} found in frontend"
            )

            # Warn about any preview models (they're unstable)
            if "preview" in model:
                pytest.warn(
                    UserWarning(
                        f"Preview model {model} found - these are unstable and may break"
                    )
                )

    def test_model_names_are_consistent(self):
        """Test that frontend offers reasonable model options"""
        frontend_models = set(get_frontend_model_names())
        backend_defaults = set(get_backend_default_models().values())

        # Frontend should include the backend default models (at minimum)
        missing_defaults = backend_defaults - frontend_models
        assert not missing_defaults, (
            f"Frontend missing backend default models: {missing_defaults}"
        )

        # All frontend models should follow valid patterns
        for model in frontend_models:
            assert re.match(r"^gemini-\d+\.\d+-(flash|pro)(-lite)?$", model), (
                f"Frontend model '{model}' doesn't follow valid naming pattern"
            )

    def test_recommended_models_are_stable(self):
        """Ensure recommended/default models are stable versions"""
        config = Configuration()

        # The reflection model is marked as "recommended" in frontend
        reflection_model = config.reflection_model
        assert "preview" not in reflection_model, (
            "Recommended reflection model should not be a preview version"
        )
        assert "flash" in reflection_model, (
            "Recommended model should be a fast flash variant"
        )


class TestModelAvailability:
    """Test suite for model availability (integration tests)"""

    @pytest.mark.integration
    def test_backend_can_initialize_default_models(self):
        """Test that backend can initialize with default model configurations"""
        import os

        from langchain_google_genai import ChatGoogleGenerativeAI

        if not os.getenv("GEMINI_API_KEY"):
            pytest.skip("GEMINI_API_KEY not set - skipping model initialization test")

        config = Configuration()
        models_to_test = [
            config.query_generator_model,
            config.reflection_model,
            config.answer_model,
        ]

        for model_name in models_to_test:
            try:
                # Try to initialize the model (doesn't make API calls)
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=0,
                    api_key=os.getenv("GEMINI_API_KEY"),
                )
                assert llm.model == model_name

            except Exception as e:
                pytest.fail(f"Failed to initialize model {model_name}: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
