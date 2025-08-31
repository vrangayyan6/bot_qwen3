import React from "react";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Zap, Cpu, CheckCircle } from "lucide-react";

interface ModelErrorDialogProps {
  isOpen: boolean;
  failedModel: string;
  onContinueWithFallback: (fallbackModel: string, rememberChoice: boolean) => void;
  onRetryWithDifferent: (newModel: string, rememberChoice: boolean) => void;
  onClose: () => void;
}

export const ModelErrorDialog: React.FC<ModelErrorDialogProps> = ({
  isOpen,
  failedModel,
  onContinueWithFallback,
  onRetryWithDifferent,
  onClose,
}) => {

  if (!isOpen) return null;

  const recommendedFallback =
    failedModel === "gemini-2.0-flash" ? "gemini-2.5-flash" : "gemini-2.0-flash";

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 max-w-lg w-full">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="h-6 w-6 text-orange-400" />
          <h2 className="text-lg font-semibold text-neutral-100">Reasoning Model Issue</h2>
        </div>

        <div className="mb-6 space-y-3">
          <p className="text-neutral-300">
            The reasoning model <span className="font-mono text-orange-400">{failedModel}</span>{" "}
            isn't available right now.
          </p>
          <p className="text-neutral-400 text-sm bg-neutral-900/50 p-3 rounded">
            💡 <strong>Good news:</strong> I can continue with your request using{" "}
            <span className="font-mono text-green-400">{recommendedFallback}</span> instead. Your
            question and conversation will be preserved.
          </p>
        </div>

        <div className="space-y-4">
          <div className="space-y-3">
            <Button
              onClick={() => onContinueWithFallback(recommendedFallback, false)}
              className="w-full justify-start bg-green-600/20 border border-green-600/30 text-green-400 hover:bg-green-600/30 py-3"
              variant="outline"
            >
              <CheckCircle className="h-5 w-5 mr-3" />
              <div className="text-left">
                <div className="font-medium">Continue with {recommendedFallback}</div>
                <div className="text-xs text-green-300 opacity-80">
                  Recommended • Just this once
                </div>
              </div>
            </Button>

            <Button
              onClick={() => onContinueWithFallback(recommendedFallback, true)}
              className="w-full justify-start bg-blue-600/20 border border-blue-600/30 text-blue-400 hover:bg-blue-600/30 py-3"
              variant="outline"
            >
              <Zap className="h-5 w-5 mr-3" />
              <div className="text-left">
                <div className="font-medium">Switch to {recommendedFallback} & Remember</div>
                <div className="text-xs text-blue-300 opacity-80">
                  Use this for all future reasoning tasks
                </div>
              </div>
            </Button>

            <details className="text-sm">
              <summary className="text-neutral-400 cursor-pointer hover:text-neutral-300 py-2">
                Advanced options...
              </summary>
              <div className="mt-3 space-y-2 pl-4 border-l-2 border-neutral-700">
                <Button
                  onClick={() => onRetryWithDifferent("gemini-2.5-pro", false)}
                  variant="outline"
                  className="w-full justify-start border-neutral-600 text-neutral-300 hover:bg-neutral-700 py-2"
                  size="sm"
                >
                  <Cpu className="h-4 w-4 mr-2" />
                  Try Gemini 2.5 Pro instead
                </Button>
                <Button
                  onClick={onClose}
                  variant="outline"
                  className="w-full border-neutral-600 text-neutral-300 hover:bg-neutral-700 py-2"
                  size="sm"
                >
                  Cancel (let me fix this manually)
                </Button>
              </div>
            </details>
          </div>
        </div>
      </div>
    </div>
  );
};
