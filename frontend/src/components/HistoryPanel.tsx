import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

interface HistoryPanelProps {
  history: any[];
  onSelectHistory: (historyItem: any) => void;
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({
  history,
  onSelectHistory,
}) => {
  return (
    <aside className="w-64 bg-neutral-900 p-4 flex flex-col">
      <h2 className="text-lg font-semibold mb-4">History</h2>
      <ScrollArea className="flex-1">
        <div className="flex flex-col gap-2">
          {history.map((item) => (
            <Button
              key={item.session_id}
              variant="ghost"
              className="w-full text-left justify-start"
              onClick={() => onSelectHistory(item)}
            >
              {item.messages[0].content}
            </Button>
          ))}
        </div>
      </ScrollArea>
    </aside>
  );
};
