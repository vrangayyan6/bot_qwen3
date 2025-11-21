import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Loader2,
  Activity,
  Info,
  Search,
  TextSearch,
  Brain,
  Pen,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useEffect, useState } from "react";

export interface ProcessedEvent {
  title: string;
  data: any;
}

interface ActivityTimelineProps {
  processedEvents: ProcessedEvent[];
  isLoading: boolean;
}

export function ActivityTimeline({
  processedEvents,
  isLoading,
}: ActivityTimelineProps) {
  const [isTimelineCollapsed, setIsTimelineCollapsed] =
    useState<boolean>(false);
  const getEventIcon = (title: string, index: number) => {
    if (index === 0 && isLoading && processedEvents.length === 0) {
      return <Loader2 className="h-4 w-4 text-indigo-400 animate-spin" />;
    }
    if (title.toLowerCase().includes("generating")) {
      return <TextSearch className="h-4 w-4 text-cyan-400" />;
    } else if (title.toLowerCase().includes("thinking")) {
      return <Loader2 className="h-4 w-4 text-indigo-400 animate-spin" />;
    } else if (title.toLowerCase().includes("reflection")) {
      return <Brain className="h-4 w-4 text-purple-400" />;
    } else if (title.toLowerCase().includes("research")) {
      return <Search className="h-4 w-4 text-blue-400" />;
    } else if (title.toLowerCase().includes("finalizing")) {
      return <Pen className="h-4 w-4 text-emerald-400" />;
    }
    return <Activity className="h-4 w-4 text-cyan-400" />;
  };

  useEffect(() => {
    if (!isLoading && processedEvents.length !== 0) {
      setIsTimelineCollapsed(true);
    }
  }, [isLoading, processedEvents]);

  return (
    <Card className="border border-indigo-500/20 rounded-lg bg-neutral-900/40 backdrop-blur-md max-h-96 shadow-lg">
      <CardHeader className="pb-3">
        <CardDescription className="flex items-center justify-between">
          <div
            className="flex items-center justify-start text-sm w-full cursor-pointer gap-2 text-indigo-300 hover:text-indigo-200 transition-colors font-medium"
            onClick={() => setIsTimelineCollapsed(!isTimelineCollapsed)}
          >
            Research
            {isTimelineCollapsed ? (
              <ChevronDown className="h-4 w-4 mr-2 text-indigo-400" />
            ) : (
              <ChevronUp className="h-4 w-4 mr-2 text-indigo-400" />
            )}
          </div>
        </CardDescription>
      </CardHeader>
      {!isTimelineCollapsed && (
        <ScrollArea className="max-h-96 overflow-y-auto">
          <CardContent>
            {isLoading && processedEvents.length === 0 && (
              <div className="relative pl-8 pb-4">
                <div className="absolute left-3 top-3.5 h-full w-0.5 bg-gradient-to-b from-indigo-500/50 to-transparent" />
                <div className="absolute left-0.5 top-2 h-5 w-5 rounded-full bg-indigo-500/30 backdrop-blur-sm flex items-center justify-center ring-4 ring-indigo-500/10">
                  <Loader2 className="h-3 w-3 text-indigo-400 animate-spin" />
                </div>
                <div>
                  <p className="text-sm text-indigo-200 font-medium">
                    Searching...
                  </p>
                </div>
              </div>
            )}
            {processedEvents.length > 0 ? (
              <div className="space-y-0">
                {processedEvents.map((eventItem, index) => (
                  <div key={index} className="relative pl-8 pb-4">
                    {index < processedEvents.length - 1 ||
                    (isLoading && index === processedEvents.length - 1) ? (
                      <div className="absolute left-3 top-3.5 h-full w-0.5 bg-gradient-to-b from-cyan-500/40 via-indigo-500/40 to-transparent" />
                    ) : null}
                    <div className="absolute left-0.5 top-2 h-6 w-6 rounded-full bg-gradient-to-br from-cyan-500/20 to-indigo-500/20 backdrop-blur-sm flex items-center justify-center ring-4 ring-cyan-500/10 border border-cyan-500/30">
                      {getEventIcon(eventItem.title, index)}
                    </div>
                    <div>
                      <p className="text-sm text-cyan-200 font-medium mb-0.5">
                        {eventItem.title}
                      </p>
                      <p className="text-xs text-neutral-300/90 leading-relaxed break-words" style={{ wordWrap: 'break-word', overflowWrap: 'anywhere' }}>
                        {typeof eventItem.data === "string"
                          ? eventItem.data
                          : Array.isArray(eventItem.data)
                          ? (eventItem.data as string[]).join(", ")
                          : JSON.stringify(eventItem.data)}
                      </p>
                    </div>
                  </div>
                ))}
                {isLoading && processedEvents.length > 0 && (
                  <div className="relative pl-8 pb-4">
                    <div className="absolute left-0.5 top-2 h-5 w-5 rounded-full bg-indigo-500/30 backdrop-blur-sm flex items-center justify-center ring-4 ring-indigo-500/10">
                      <Loader2 className="h-3 w-3 text-indigo-400 animate-spin" />
                    </div>
                    <div>
                      <p className="text-sm text-indigo-200 font-medium">
                        Searching...
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ) : !isLoading ? ( // Only show "No activity" if not loading and no events
              <div className="flex flex-col items-center justify-center h-full text-neutral-400 pt-10">
                <Info className="h-6 w-6 mb-3 text-indigo-400/50" />
                <p className="text-sm text-neutral-300">No activity to display.</p>
                <p className="text-xs text-neutral-500 mt-1">
                  Timeline will update during processing.
                </p>
              </div>
            ) : null}
          </CardContent>
        </ScrollArea>
      )}
    </Card>
  );
}
