import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { MessageSquare, Trash2, X, Clock, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  metadata: Record<string, any>;
}

interface ConversationHistoryProps {
  onSelectConversation: (conversationId: string) => void;
  onClose: () => void;
  currentConversationId?: string;
}

export function ConversationHistory({
  onSelectConversation,
  onClose,
  currentConversationId,
}: ConversationHistoryProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/conversations");
      if (!response.ok) {
        throw new Error("Failed to fetch conversations");
      }
      const data = await response.json();
      setConversations(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load conversations");
    } finally {
      setLoading(false);
    }
  };

  const deleteConversation = async (conversationId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    
    if (!confirm("Are you sure you want to delete this conversation?")) {
      return;
    }

    try {
      const response = await fetch(`/api/conversation/${conversationId}`, {
        method: "DELETE",
      });
      
      if (!response.ok) {
        throw new Error("Failed to delete conversation");
      }
      
      // Refresh the list
      fetchConversations();
    } catch (err) {
      console.error("Error deleting conversation:", err);
      alert("Failed to delete conversation");
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } else if (diffInHours < 48) {
      return "Yesterday";
    } else {
      return date.toLocaleDateString([], { month: "short", day: "numeric" });
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl max-h-[80vh] bg-neutral-900/95 border-indigo-500/30 shadow-2xl">
        <CardHeader className="border-b border-indigo-500/20">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl font-bold text-indigo-300">
                Conversation History
              </CardTitle>
              <CardDescription className="text-neutral-400 mt-1">
                Resume or delete previous conversations
              </CardDescription>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(80vh-140px)]">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-indigo-400" />
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-12 text-neutral-400">
                <p className="mb-4">{error}</p>
                <Button onClick={fetchConversations} variant="outline">
                  Retry
                </Button>
              </div>
            ) : conversations.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-neutral-400">
                <MessageSquare className="h-12 w-12 mb-3 opacity-50" />
                <p className="text-lg">No conversations yet</p>
                <p className="text-sm mt-1">Start a new conversation to see it here</p>
              </div>
            ) : (
              <div className="p-4 space-y-2">
                {conversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    onClick={() => onSelectConversation(conversation.id)}
                    className={`group relative p-4 rounded-lg border transition-all cursor-pointer ${
                      currentConversationId === conversation.id
                        ? "bg-indigo-500/20 border-indigo-500/50 shadow-md"
                        : "bg-neutral-800/40 border-neutral-700/50 hover:bg-neutral-800/60 hover:border-indigo-500/30"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2">
                          <MessageSquare className="h-4 w-4 text-indigo-400 flex-shrink-0" />
                          <h3 className="text-sm font-medium text-neutral-200 truncate">
                            {conversation.title}
                          </h3>
                          {currentConversationId === conversation.id && (
                            <Badge className="bg-indigo-500/20 text-indigo-300 border-indigo-500/30 text-xs">
                              Current
                            </Badge>
                          )}
                        </div>
                        <div className="flex items-center gap-3 text-xs text-neutral-400">
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {formatDate(conversation.updated_at)}
                          </span>
                          <span>
                            {conversation.message_count}{" "}
                            {conversation.message_count === 1 ? "message" : "messages"}
                          </span>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => deleteConversation(conversation.id, e)}
                        className="opacity-0 group-hover:opacity-100 transition-opacity text-red-400 hover:text-red-300 hover:bg-red-500/10 flex-shrink-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
