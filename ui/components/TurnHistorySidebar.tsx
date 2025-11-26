'use client';

interface TurnHistorySidebarProps {
  totalTurns: number;
  selectedTurn: number | 'summary' | null;
  onSelectTurn: (turn: number | 'summary') => void;
}

export default function TurnHistorySidebar({
  totalTurns,
  selectedTurn,
  onSelectTurn,
}: TurnHistorySidebarProps) {
  return (
    <div className="w-1/4 border-r border-beige-300 bg-beige-50 flex flex-col">
      <div className="p-4 border-b border-beige-300">
        <h2 className="text-sm font-medium text-beige-900">Run Summary</h2>
      </div>
      <button
        onClick={() => onSelectTurn('summary')}
        className={`w-full text-left p-3 border-b border-beige-200 hover:bg-beige-100 transition-colors ${
          selectedTurn === 'summary' ? 'bg-beige-200' : ''
        }`}
      >
        <div className="text-sm font-medium text-beige-900">Summary</div>
      </button>
      <div className="flex-1 overflow-y-auto">
        {Array.from({ length: totalTurns }, (_, i) => (
          <button
            key={i}
            onClick={() => onSelectTurn(i)}
            className={`w-full text-left p-3 border-b border-beige-200 hover:bg-beige-100 transition-colors ${
              selectedTurn === i ? 'bg-beige-200' : ''
            }`}
          >
            <div className="text-sm font-medium text-beige-900">
              Turn {i + 1}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

