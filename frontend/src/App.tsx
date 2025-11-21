import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";
import { useState, useEffect, useRef, useCallback } from "react";
import { ProcessedEvent } from "@/components/ActivityTimeline";
import { WelcomeScreen } from "@/components/WelcomeScreen";
import { ChatMessagesView } from "@/components/ChatMessagesView";
import { ConversationHistory } from "@/components/ConversationHistory";
import { Button } from "@/components/ui/button";
import { History } from "lucide-react";

export default function App() {
  const [showHistory, setShowHistory] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<
    string | null
  >(null);
  const [processedEventsTimeline, setProcessedEventsTimeline] = useState<
    ProcessedEvent[]
  >([]);
  const [historicalActivities, setHistoricalActivities] = useState<
    Record<string, ProcessedEvent[]>
  >({});
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const hasFinalizeEventOccurredRef = useRef(false);
  const [error, setError] = useState<string | null>(null);
  const thread = useStream<{
    messages: Message[];
    initial_search_query_count: number;
    max_research_loops: number;
    reasoning_model: string;
  }>({
    apiUrl: import.meta.env.DEV
      ? "http://localhost:2024"
      : "http://localhost:8123",
    assistantId: "agent",
    messagesKey: "messages",
    onUpdateEvent: (event: any) => {
      let processedEvent: ProcessedEvent | null = null;
      if (event.generate_query) {
        processedEvent = {
          title: "Generating Search Queries",
          data: event.generate_query?.search_query?.join(", ") || "",
        };
      } else if (event.web_research) {
        const sources = event.web_research.sources_gathered || [];
        const numSources = sources.length;
        const uniqueLabels = [
          ...new Set(sources.map((s: any) => s.label).filter(Boolean)),
        ];
        const exampleLabels = uniqueLabels.slice(0, 3).join(", ");
        processedEvent = {
          title: "Web Research",
          data: `Gathered ${numSources} sources. Related to: ${
            exampleLabels || "N/A"
          }.`,
        };
      } else if (event.reflection) {
        processedEvent = {
          title: "Reflection",
          data: "Analysing Web Research Results",
        };
      } else if (event.finalize_answer) {
        processedEvent = {
          title: "Finalizing Answer",
          data: "Composing and presenting the final answer.",
        };
        hasFinalizeEventOccurredRef.current = true;
      }
      if (processedEvent) {
        setProcessedEventsTimeline((prevEvents) => [
          ...prevEvents,
          processedEvent!,
        ]);
      }
    },
    onError: (error: any) => {
      setError(error.message);
    },
  });

  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollViewport = scrollAreaRef.current.querySelector(
        "[data-radix-scroll-area-viewport]"
      );
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight;
      }
    }
  }, [thread.messages]);

  useEffect(() => {
    if (
      hasFinalizeEventOccurredRef.current &&
      !thread.isLoading &&
      thread.messages.length > 0
    ) {
      const lastMessage = thread.messages[thread.messages.length - 1];
      if (lastMessage && lastMessage.type === "ai" && lastMessage.id) {
        setHistoricalActivities((prev) => ({
          ...prev,
          [lastMessage.id!]: [...processedEventsTimeline],
        }));
      }
      hasFinalizeEventOccurredRef.current = false;
    }
  }, [thread.messages, thread.isLoading, processedEventsTimeline]);

  const createNewConversation = useCallback(async () => {
    try {
      const response = await fetch("/api/conversation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: "New Conversation",
        }),
      });
      
      if (!response.ok) {
        throw new Error("Failed to create conversation");
      }
      
      const data = await response.json();
      setCurrentConversationId(data.id);
      return data.id;
    } catch (error) {
      console.error("Error creating conversation:", error);
      return null;
    }
  }, []);

  const saveMessage = useCallback(
    async (role: string, content: string, conversationId: string) => {
      try {
        await fetch(`/api/conversation/${conversationId}/message`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role,
            content,
          }),
        });
      } catch (error) {
        console.error("Error saving message:", error);
      }
    },
    []
  );

  const loadConversation = useCallback(
    async (conversationId: string) => {
      try {
        const response = await fetch(
          `/api/conversation/${conversationId}/messages`
        );
        if (!response.ok) {
          throw new Error("Failed to load conversation");
        }

        const messages = await response.json();
        const langchainMessages: Message[] = messages.map((msg: any) => ({
          type: msg.role === "human" ? "human" : "ai",
          content: msg.content,
          id: msg.id.toString(),
        }));

        setCurrentConversationId(conversationId);
        thread.submit({
          messages: langchainMessages,
          initial_search_query_count: 3,
          max_research_loops: 3,
          reasoning_model: "gemini-2.0-flash-thinking-exp-01-21",
        });
        setShowHistory(false);
      } catch (error) {
        console.error("Error loading conversation:", error);
        alert("Failed to load conversation");
      }
    },
    [thread]
  );

  const handleSubmit = useCallback(
    async (submittedInputValue: string, effort: string, model: string) => {
      if (!submittedInputValue.trim()) return;
      setProcessedEventsTimeline([]);
      hasFinalizeEventOccurredRef.current = false;

      // Create a new conversation if we don't have one
      let conversationId = currentConversationId;
      if (!conversationId) {
        conversationId = await createNewConversation();
        if (!conversationId) {
          alert("Failed to create conversation");
          return;
        }
      }

      // Save the user message
      await saveMessage("human", submittedInputValue, conversationId);

      // convert effort to, initial_search_query_count and max_research_loops
      let initial_search_query_count = 0;
      let max_research_loops = 0;
      switch (effort) {
        case "low":
          initial_search_query_count = 1;
          max_research_loops = 1;
          break;
        case "medium":
          initial_search_query_count = 3;
          max_research_loops = 3;
          break;
        case "high":
          initial_search_query_count = 5;
          max_research_loops = 10;
          break;
      }

      const newMessages: Message[] = [
        ...(thread.messages || []),
        {
          type: "human",
          content: submittedInputValue,
          id: Date.now().toString(),
        },
      ];
      thread.submit({
        messages: newMessages,
        initial_search_query_count: initial_search_query_count,
        max_research_loops: max_research_loops,
        reasoning_model: model,
      });
    },
    [thread, currentConversationId, createNewConversation, saveMessage]
  );

  // Save AI messages when they arrive
  useEffect(() => {
    if (
      currentConversationId &&
      thread.messages.length > 0 &&
      !thread.isLoading
    ) {
      const lastMessage = thread.messages[thread.messages.length - 1];
      if (lastMessage && lastMessage.type === "ai") {
        saveMessage("ai", lastMessage.content as string, currentConversationId);
      }
    }
  }, [thread.messages, thread.isLoading, currentConversationId, saveMessage]);

  const handleCancel = useCallback(() => {
    thread.stop();
    window.location.reload();
  }, [thread]);

  const handleNewConversation = useCallback(() => {
    setCurrentConversationId(null);
    window.location.reload();
  }, []);

  return (
    <div className="flex h-screen bg-neutral-800 text-neutral-100 font-sans antialiased">
      {/* History Button - Fixed Position */}
      <Button
        onClick={() => setShowHistory(true)}
        className="fixed top-4 left-4 z-40 bg-indigo-600/80 backdrop-blur-sm hover:bg-indigo-600 text-white shadow-lg border border-indigo-500/30"
        size="default"
      >
        <History className="h-4 w-4 mr-2" />
        History
      </Button>

      {/* New Conversation Button - Show when in conversation */}
      {thread.messages.length > 0 && (
        <Button
          onClick={handleNewConversation}
          className="fixed top-4 left-32 z-40 bg-cyan-600/80 backdrop-blur-sm hover:bg-cyan-600 text-white shadow-lg border border-cyan-500/30"
          size="default"
        >
          New Chat
        </Button>
      )}

      {/* Conversation History Modal */}
      {showHistory && (
        <ConversationHistory
          onSelectConversation={loadConversation}
          onClose={() => setShowHistory(false)}
          currentConversationId={currentConversationId || undefined}
        />
      )}

      <main className="h-full w-full max-w-4xl mx-auto">
          {thread.messages.length === 0 ? (
            <WelcomeScreen
              handleSubmit={handleSubmit}
              isLoading={thread.isLoading}
              onCancel={handleCancel}
            />
          ) : error ? (
            <div className="flex flex-col items-center justify-center h-full">
              <div className="flex flex-col items-center justify-center gap-4">
                <h1 className="text-2xl text-red-400 font-bold">Error</h1>
                <p className="text-red-400">{JSON.stringify(error)}</p>

                <Button
                  variant="destructive"
                  onClick={() => window.location.reload()}
                >
                  Retry
                </Button>
              </div>
            </div>
          ) : (
            <ChatMessagesView
              messages={thread.messages}
              isLoading={thread.isLoading}
              scrollAreaRef={scrollAreaRef}
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              liveActivityEvents={processedEventsTimeline}
              historicalActivities={historicalActivities}
            />
          )}
      </main>
    </div>
  );
}
