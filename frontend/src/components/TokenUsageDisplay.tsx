import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Coins,
  TrendingUp,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Search,
  Brain,
  Pen,
} from "lucide-react";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";

export interface TokenUsageRecord {
  node_name: string;
  input_tokens: number;
  output_tokens: number;
  model: string;
}

interface TokenUsageDisplayProps {
  tokenRecords: TokenUsageRecord[];
  isLoading: boolean;
}

const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  "gemini-2.0-flash": { input: 0.075, output: 0.3 },
  "gemini-2.5-flash": { input: 0.075, output: 0.3 },
  "gemini-2.5-flash-preview-04-17": { input: 0.075, output: 0.3 },
  "gemini-2.5-pro": { input: 1.25, output: 5.0 },
  "gemini-2.5-pro-preview-05-06": { input: 1.25, output: 5.0 },
  default: { input: 0.075, output: 0.3 },
};

const getNodeIcon = (nodeName: string) => {
  if (nodeName.toLowerCase().includes("generate")) {
    return <Sparkles className="h-4 w-4 text-yellow-400" />;
  } else if (nodeName.toLowerCase().includes("research")) {
    return <Search className="h-4 w-4 text-blue-400" />;
  } else if (nodeName.toLowerCase().includes("reflection")) {
    return <Brain className="h-4 w-4 text-purple-400" />;
  } else if (nodeName.toLowerCase().includes("finalize")) {
    return <Pen className="h-4 w-4 text-green-400" />;
  }
  return <Coins className="h-4 w-4 text-neutral-400" />;
};

const calculateCost = (
  inputTokens: number,
  outputTokens: number,
  model: string
): number => {
  const pricing = MODEL_PRICING[model] || MODEL_PRICING.default;
  const inputCost = (inputTokens / 1000000) * pricing.input;
  const outputCost = (outputTokens / 1000000) * pricing.output;
  return inputCost + outputCost;
};

export function TokenUsageDisplay({
  tokenRecords,
  isLoading,
}: TokenUsageDisplayProps) {
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);

  const totals = tokenRecords.reduce(
    (acc, record) => {
      acc.inputTokens += record.input_tokens;
      acc.outputTokens += record.output_tokens;
      acc.totalTokens += record.input_tokens + record.output_tokens;
      acc.cost += calculateCost(
        record.input_tokens,
        record.output_tokens,
        record.model
      );
      return acc;
    },
    { inputTokens: 0, outputTokens: 0, totalTokens: 0, cost: 0 }
  );

  if (tokenRecords.length === 0 && !isLoading) {
    return null;
  }

  return (
    <Card className="border-none rounded-lg bg-neutral-700 mt-2">
      <CardHeader>
        <CardDescription className="flex items-center justify-between">
          <div
            className="flex items-center justify-start text-sm w-full cursor-pointer gap-2 text-neutral-100"
            onClick={() => setIsCollapsed(!isCollapsed)}
          >
            <Coins className="h-4 w-4" />
            Token Usage
            {totals.totalTokens > 0 && (
              <Badge variant="secondary" className="ml-2 text-xs">
                {totals.totalTokens.toLocaleString()} tokens
              </Badge>
            )}
            {totals.cost > 0 && (
              <Badge variant="secondary" className="ml-1 text-xs">
                ~${totals.cost.toFixed(4)}
              </Badge>
            )}
            {isCollapsed ? (
              <ChevronDown className="h-4 w-4 ml-auto" />
            ) : (
              <ChevronUp className="h-4 w-4 ml-auto" />
            )}
          </div>
        </CardDescription>
      </CardHeader>
      {!isCollapsed && (
        <ScrollArea className="max-h-64 overflow-y-auto">
          <CardContent>
            {tokenRecords.length > 0 ? (
              <div className="space-y-3">
                <div className="space-y-2">
                  {tokenRecords.map((record, index) => {
                    const nodeCost = calculateCost(
                      record.input_tokens,
                      record.output_tokens,
                      record.model
                    );
                    return (
                      <div
                        key={index}
                        className="relative pl-8 pb-2 border-l-2 border-neutral-600 last:border-l-0"
                      >
                        <div className="absolute left-[-13px] top-1 h-6 w-6 rounded-full bg-neutral-600 flex items-center justify-center ring-4 ring-neutral-700">
                          {getNodeIcon(record.node_name)}
                        </div>
                        <div className="space-y-1">
                          <div className="flex items-center justify-between">
                            <p className="text-sm text-neutral-200 font-medium">
                              {record.node_name
                                .split("_")
                                .map(
                                  (word) =>
                                    word.charAt(0).toUpperCase() + word.slice(1)
                                )
                                .join(" ")}
                            </p>
                            <Badge
                              variant="outline"
                              className="text-xs text-neutral-400 border-neutral-600"
                            >
                              {record.model.replace("gemini-", "")}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-3 text-xs text-neutral-400">
                            <span>
                              ↓ {record.input_tokens.toLocaleString()} in
                            </span>
                            <span>
                              ↑ {record.output_tokens.toLocaleString()} out
                            </span>
                            {nodeCost > 0 && (
                              <span className="ml-auto text-green-400">
                                ${nodeCost.toFixed(4)}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {tokenRecords.length > 1 && (
                  <div className="pt-3 border-t border-neutral-600">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2 text-neutral-200 font-semibold">
                        <TrendingUp className="h-4 w-4" />
                        Total
                      </div>
                      <div className="flex items-center gap-3 text-xs">
                        <span className="text-neutral-400">
                          {totals.totalTokens.toLocaleString()} tokens
                        </span>
                        {totals.cost > 0 && (
                          <span className="text-green-400 font-semibold">
                            ${totals.cost.toFixed(4)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center h-20 text-neutral-500">
                <p className="text-sm">
                  {isLoading
                    ? "Calculating token usage..."
                    : "No token data available"}
                </p>
              </div>
            )}
          </CardContent>
        </ScrollArea>
      )}
    </Card>
  );
}
