import type React from "react";
import type { Message } from "@langchain/langgraph-sdk";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, Copy, CopyCheck } from "lucide-react";
import { InputForm } from "@/components/InputForm";
import { Button } from "@/components/ui/button";
import { useState, ReactNode, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import {
  ActivityTimeline,
  ProcessedEvent,
} from "@/components/ActivityTimeline"; // Assuming ActivityTimeline is in the same dir or adjust path

const Star = ({ delay }: { delay: number }) => (
  <div
    className="absolute w-1 h-1 bg-white rounded-full opacity-70 animate-fall"
    style={{
      left: `${Math.random() * 100}%`,
      animationDelay: `${delay}s`,
      animationDuration: `${3 + Math.random() * 4}s`,
    }}
  />
);

const ShootingStar = ({ delay }: { delay: number }) => (
  <div
    className="absolute w-0 h-0 border-l-[0px] border-l-transparent border-r-[2px] border-r-white transform rotate-[-45deg] opacity-0 animate-shoot"
    style={{
      top: `${Math.random() * 20}%`,
      left: "100%",
      animationDelay: `${delay}s`,
      animationDuration: `${1 + Math.random() * 2}s`,
    }}
  />
);

const Sunray = ({ delay, angle }: { delay: number; angle: number }) => (
  <div
    className="absolute top-0 left-1/2 w-[2px] h-full origin-top opacity-0 animate-sunray"
    style={{
      background: 'linear-gradient(to bottom, rgba(255, 220, 150, 0.4), transparent)',
      transform: `rotate(${angle}deg)`,
      animationDelay: `${delay}s`,
    }}
  />
);

// Markdown component props type from former ReportView
type MdComponentProps = {
  className?: string;
  children?: ReactNode;
  [key: string]: any;
};

// Markdown components (from former ReportView.tsx)
const mdComponents = {
  h1: ({ className, children, ...props }: MdComponentProps) => (
    <h1 className={cn("text-2xl font-bold mt-4 mb-2", className)} {...props}>
      {children}
    </h1>
  ),
  h2: ({ className, children, ...props }: MdComponentProps) => (
    <h2 className={cn("text-xl font-bold mt-3 mb-2", className)} {...props}>
      {children}
    </h2>
  ),
  h3: ({ className, children, ...props }: MdComponentProps) => (
    <h3 className={cn("text-lg font-bold mt-3 mb-1", className)} {...props}>
      {children}
    </h3>
  ),
  p: ({ className, children, ...props }: MdComponentProps) => (
    <p className={cn("mb-3 leading-7 break-words", className)} style={{ wordWrap: 'break-word', overflowWrap: 'anywhere' }} {...props}>
      {children}
    </p>
  ),
  a: ({ className, children, href, ...props }: MdComponentProps) => (
    <Badge className="text-xs mx-0.5">
      <a
        className={cn("text-blue-400 hover:text-blue-300 text-xs", className)}
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        {...props}
      >
        {children}
      </a>
    </Badge>
  ),
  ul: ({ className, children, ...props }: MdComponentProps) => (
    <ul className={cn("list-disc pl-6 mb-3", className)} {...props}>
      {children}
    </ul>
  ),
  ol: ({ className, children, ...props }: MdComponentProps) => (
    <ol className={cn("list-decimal pl-6 mb-3", className)} {...props}>
      {children}
    </ol>
  ),
  li: ({ className, children, ...props }: MdComponentProps) => (
    <li className={cn("mb-1", className)} {...props}>
      {children}
    </li>
  ),
  blockquote: ({ className, children, ...props }: MdComponentProps) => (
    <blockquote
      className={cn(
        "border-l-4 border-neutral-600 pl-4 italic my-3 text-sm",
        className
      )}
      {...props}
    >
      {children}
    </blockquote>
  ),
  code: ({ className, children, ...props }: MdComponentProps) => (
    <code
      className={cn(
        "bg-neutral-900 rounded px-1 py-0.5 font-mono text-xs",
        className
      )}
      {...props}
    >
      {children}
    </code>
  ),
  pre: ({ className, children, ...props }: MdComponentProps) => (
    <pre
      className={cn(
        "bg-neutral-900 p-3 rounded-lg overflow-x-auto font-mono text-xs my-3",
        className
      )}
      {...props}
    >
      {children}
    </pre>
  ),
  hr: ({ className, ...props }: MdComponentProps) => (
    <hr className={cn("border-neutral-600 my-4", className)} {...props} />
  ),
  table: ({ className, children, ...props }: MdComponentProps) => (
    <div className="my-3 overflow-x-auto">
      <table className={cn("border-collapse w-full", className)} {...props}>
        {children}
      </table>
    </div>
  ),
  th: ({ className, children, ...props }: MdComponentProps) => (
    <th
      className={cn(
        "border border-neutral-600 px-3 py-2 text-left font-bold",
        className
      )}
      {...props}
    >
      {children}
    </th>
  ),
  td: ({ className, children, ...props }: MdComponentProps) => (
    <td
      className={cn("border border-neutral-600 px-3 py-2", className)}
      {...props}
    >
      {children}
    </td>
  ),
};

// Props for HumanMessageBubble
interface HumanMessageBubbleProps {
  message: Message;
  mdComponents: typeof mdComponents;
}

// HumanMessageBubble Component
const HumanMessageBubble: React.FC<HumanMessageBubbleProps> = ({
  message,
  mdComponents,
}) => {
  return (
    <div
      className={`text-white rounded-3xl break-words word-wrap min-h-7 bg-neutral-700 max-w-[95%] px-4 pt-3 rounded-br-lg overflow-wrap-anywhere`}
      style={{ wordWrap: 'break-word', overflowWrap: 'anywhere' }}
    >
      <ReactMarkdown components={mdComponents}>
        {typeof message.content === "string"
          ? message.content
          : JSON.stringify(message.content)}
      </ReactMarkdown>
    </div>
  );
};

// Props for AiMessageBubble
interface AiMessageBubbleProps {
  message: Message;
  historicalActivity: ProcessedEvent[] | undefined;
  liveActivity: ProcessedEvent[] | undefined;
  isLastMessage: boolean;
  isOverallLoading: boolean;
  mdComponents: typeof mdComponents;
  handleCopy: (text: string, messageId: string) => void;
  copiedMessageId: string | null;
}

// AiMessageBubble Component
const AiMessageBubble: React.FC<AiMessageBubbleProps> = ({
  message,
  historicalActivity,
  liveActivity,
  isLastMessage,
  isOverallLoading,
  mdComponents,
  handleCopy,
  copiedMessageId,
}) => {
  // Determine which activity events to show and if it's for a live loading message
  const activityForThisBubble =
    isLastMessage && isOverallLoading ? liveActivity : historicalActivity;
  const isLiveActivityForThisBubble = isLastMessage && isOverallLoading;

  return (
    <div className={`relative break-words flex flex-col overflow-wrap-anywhere`} style={{ wordWrap: 'break-word', overflowWrap: 'anywhere' }}>
      {activityForThisBubble && activityForThisBubble.length > 0 && (
        <div className="mb-3 border-b border-neutral-700 pb-3 text-xs">
          <ActivityTimeline
            processedEvents={activityForThisBubble}
            isLoading={isLiveActivityForThisBubble}
          />
        </div>
      )}
      <ReactMarkdown components={mdComponents}>
        {typeof message.content === "string"
          ? message.content
          : JSON.stringify(message.content)}
      </ReactMarkdown>
      <Button
        variant="default"
        className={`cursor-pointer bg-neutral-700 border-neutral-600 text-neutral-300 self-end ${
          message.content.length > 0 ? "visible" : "hidden"
        }`}
        onClick={() =>
          handleCopy(
            typeof message.content === "string"
              ? message.content
              : JSON.stringify(message.content),
            message.id!
          )
        }
      >
        {copiedMessageId === message.id ? "Copied" : "Copy"}
        {copiedMessageId === message.id ? <CopyCheck /> : <Copy />}
      </Button>
    </div>
  );
};

interface ChatMessagesViewProps {
  messages: Message[];
  isLoading: boolean;
  scrollAreaRef: React.RefObject<HTMLDivElement | null>;
  onSubmit: (inputValue: string, effort: string, model: string) => void;
  onCancel: () => void;
  liveActivityEvents: ProcessedEvent[];
  historicalActivities: Record<string, ProcessedEvent[]>;
}

export function ChatMessagesView({
  messages,
  isLoading,
  scrollAreaRef,
  onSubmit,
  onCancel,
  liveActivityEvents,
  historicalActivities,
}: ChatMessagesViewProps) {
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null);
  const [stars, setStars] = useState<number[]>([]);

  useEffect(() => {
    // Generate 50 random stars for background twinkling/falling
    const starDelays = Array.from({ length: 50 }, (_, i) => i * 0.1);
    setStars(starDelays);
  }, []);

  const sunrays = Array.from({ length: 12 }, (_, i) => ({
    angle: (i * 30) - 165,
    delay: i * 0.5,
  }));

  const handleCopy = async (text: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedMessageId(messageId);
      setTimeout(() => setCopiedMessageId(null), 2000); // Reset after 2 seconds
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };
  return (
    <div className="flex flex-col h-full relative overflow-hidden">
      {/* Space Background with Darker Nebula Gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-black via-indigo-950/30 to-slate-900/40 pointer-events-none">
        {/* Twinkling Stars */}
        {stars.map((delay, i) => (
          <div
            key={`twinkle-${i}`}
            className="absolute w-[2px] h-[2px] bg-white rounded-full opacity-40 animate-twinkle"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${delay}s`,
            }}
          />
        ))}
        
        {/* Falling Stars */}
        {stars.slice(0, 20).map((delay, i) => (
          <Star key={`fall-${i}`} delay={delay} />
        ))}
        
        {/* Shooting Stars */}
        {stars.slice(0, 5).map((delay, i) => (
          <ShootingStar key={`shoot-${i}`} delay={delay * 2} />
        ))}
        
        {/* Sunrays */}
        <div className="absolute inset-0 flex items-center justify-center overflow-hidden">
          {sunrays.map((ray, i) => (
            <Sunray key={`sunray-${i}`} delay={ray.delay} angle={ray.angle} />
          ))}
        </div>
        
        {/* Subtle Solar System Orb - Central Glow */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-32 h-32 bg-gradient-to-r from-amber-400/15 via-orange-400/10 to-yellow-500/15 rounded-full blur-xl animate-pulse-slow opacity-25" />
        </div>
        
        {/* Orbiting Planet (subtle) */}
        <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-gradient-to-r from-blue-400/40 to-indigo-500/40 rounded-full animate-orbit opacity-50" />
      </div>
      <ScrollArea className="flex-1 overflow-y-auto relative z-10" ref={scrollAreaRef}>
        <div className="p-4 md:p-6 space-y-2 max-w-full mx-auto pt-16 px-4 md:px-8 lg:px-12">
          {messages.map((message, index) => {
            const isLast = index === messages.length - 1;
            return (
              <div key={message.id || `msg-${index}`} className="space-y-3">
                <div
                  className={`flex items-start gap-3 ${
                    message.type === "human" ? "justify-end" : ""
                  }`}
                >
                  {message.type === "human" ? (
                    <HumanMessageBubble
                      message={message}
                      mdComponents={mdComponents}
                    />
                  ) : (
                    <AiMessageBubble
                      message={message}
                      historicalActivity={historicalActivities[message.id!]}
                      liveActivity={liveActivityEvents} // Pass global live events
                      isLastMessage={isLast}
                      isOverallLoading={isLoading} // Pass global loading state
                      mdComponents={mdComponents}
                      handleCopy={handleCopy}
                      copiedMessageId={copiedMessageId}
                    />
                  )}
                </div>
              </div>
            );
          })}
          {isLoading &&
            (messages.length === 0 ||
              messages[messages.length - 1].type === "human") && (
              <div className="flex items-start gap-3 mt-3">
                {" "}
                {/* AI message row structure */}
                <div className="relative group max-w-[95%] rounded-xl p-3 shadow-sm break-words bg-neutral-800 text-neutral-100 rounded-bl-none w-full min-h-[56px]" style={{ wordWrap: 'break-word', overflowWrap: 'anywhere' }}>
                  {liveActivityEvents.length > 0 ? (
                    <div className="text-xs">
                      <ActivityTimeline
                        processedEvents={liveActivityEvents}
                        isLoading={true}
                      />
                    </div>
                  ) : (
                    <div className="flex items-center justify-start h-full">
                      <Loader2 className="h-5 w-5 animate-spin text-neutral-400 mr-2" />
                      <span>Processing...</span>
                    </div>
                  )}
                </div>
              </div>
            )}
        </div>
      </ScrollArea>
      <div className="relative z-10">
        <InputForm
          onSubmit={onSubmit}
          isLoading={isLoading}
          onCancel={onCancel}
          hasHistory={messages.length > 0}
        />
      </div>

      <style>{`
        @keyframes fall {
          0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
          }
        }
        @keyframes shoot {
          0% {
            opacity: 0;
            transform: translateX(-100vw) translateY(0);
          }
          50% {
            opacity: 1;
          }
          100% {
            opacity: 0;
            transform: translateX(-200vw) translateY(-50vh);
          }
        }
        @keyframes twinkle {
          0%, 100% { opacity: 0.4; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.2); }
        }
        @keyframes orbit {
          0% { transform: rotate(0deg) translateX(100px) rotate(0deg); }
          100% { transform: rotate(360deg) translateX(100px) rotate(-360deg); }
        }
        @keyframes pulse-slow {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(1.1); }
        }
        @keyframes sunray {
          0% {
            opacity: 0;
            height: 0;
          }
          20% {
            opacity: 0.3;
            height: 50%;
          }
          40% {
            opacity: 0.5;
            height: 100%;
          }
          60% {
            opacity: 0.3;
            height: 100%;
          }
          100% {
            opacity: 0;
            height: 100%;
          }
        }
        .animate-fall {
          animation: fall linear infinite;
        }
        .animate-shoot {
          animation: shoot linear infinite;
        }
        .animate-twinkle {
          animation: twinkle 2s ease-in-out infinite;
        }
        .animate-orbit {
          animation: orbit 20s linear infinite;
        }
        .animate-pulse-slow {
          animation: pulse-slow 4s ease-in-out infinite;
        }
        .animate-sunray {
          animation: sunray 8s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
