/**
 * Frontend regression tests for model configuration validation.
 *
 * These tests prevent frontend/backend model mismatches by ensuring:
 * 1. No deprecated preview models in frontend source code
 * 2. Model names follow stable naming conventions
 * 3. Default models are reasonable choices
 */

import { describe, it, expect } from "vitest";
import { readFileSync } from "fs";
import { join } from "path";

// Read the InputForm source code to validate model configurations
function getInputFormSource(): string {
  const inputFormPath = join(process.cwd(), "src", "components", "InputForm.tsx");
  return readFileSync(inputFormPath, "utf-8");
}

// Extract model names from source code
function getModelNamesFromSource(source: string): string[] {
  const modelPattern = /value="(gemini-[^"]+)"/g;
  const matches = [...source.matchAll(modelPattern)];
  return matches.map(match => match[1]);
}

describe("Model Configuration Validation", () => {
  it("should not contain deprecated preview models in source code", () => {
    const source = getInputFormSource();

    // Check that deprecated models are not in the source code
    const deprecatedModels = ["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-preview-05-06"];

    deprecatedModels.forEach(model => {
      expect(source).not.toContain(model);
    });
  });

  it("should only offer stable model versions", () => {
    const models = getModelNamesFromSource(getInputFormSource());

    // All models should be stable versions
    const stableModels = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro"];

    // Check that we have these stable models
    stableModels.forEach(model => {
      expect(models).toContain(model);
    });
  });

  it("should not contain any preview models in source", () => {
    const models = getModelNamesFromSource(getInputFormSource());

    models.forEach(model => {
      // Should not contain preview versions
      expect(model).not.toMatch(/preview/);
      // Should not contain date patterns (deprecated models)
      expect(model).not.toMatch(/\d{2}-\d{2}/);
    });
  });

  it("should follow consistent model naming patterns", () => {
    const models = getModelNamesFromSource(getInputFormSource());

    models.forEach(model => {
      // All models should follow gemini-X.Y-variant pattern
      expect(model).toMatch(/^gemini-\d+\.\d+-(flash|pro)(-lite)?$/);
    });
  });

  it("should use reasonable default model", () => {
    const source = getInputFormSource();

    // Check the default reasoning model state
    const defaultMatch = source.match(/setReasoningModel\] = useState\("([^"]+)"\)/);
    expect(defaultMatch).toBeTruthy();

    if (defaultMatch) {
      const defaultModel = defaultMatch[1];

      // Default should be stable
      expect(defaultModel).not.toMatch(/preview/);
      expect(defaultModel).not.toMatch(/\d{2}-\d{2}/);
      expect(defaultModel).toMatch(/^gemini-\d+\.\d+-(flash|pro)(-lite)?$/);
    }
  });
});

describe("Model Error Handling", () => {
  it("should provide fallback to stable models in error dialog", () => {
    // Read ModelErrorDialog source to check fallback model
    const errorDialogPath = join(process.cwd(), "src", "components", "ModelErrorDialog.tsx");
    const source = readFileSync(errorDialogPath, "utf-8");

    // Look for the dynamic fallback model logic
    const fallbackMatch = source.match(/recommendedFallback =\s*\n?\s*failedModel === "([^"]+)"/);
    expect(fallbackMatch).toBeTruthy();

    if (fallbackMatch) {
      const fallbackModel = fallbackMatch[1];

      // Fallback should be stable
      expect(fallbackModel).toMatch(/^gemini-\d+\.\d+-(flash|pro)(-lite)?$/);
      expect(fallbackModel).not.toMatch(/preview/);
      expect(fallbackModel).not.toMatch(/\d{2}-\d{2}/);
    }
  });

  it("should use stable models in retry options", () => {
    const errorDialogPath = join(process.cwd(), "src", "components", "ModelErrorDialog.tsx");
    const source = readFileSync(errorDialogPath, "utf-8");

    // Look for retry model options
    const retryMatches = [...source.matchAll(/onRetryWithDifferent\("([^"]+)"/g)];

    retryMatches.forEach(match => {
      const retryModel = match[1];

      // Retry models should be stable
      expect(retryModel).toMatch(/^gemini-\d+\.\d+-(flash|pro)(-lite)?$/);
      expect(retryModel).not.toMatch(/preview/);
      expect(retryModel).not.toMatch(/\d{2}-\d{2}/);
    });
  });
});
