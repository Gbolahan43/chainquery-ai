import { useState, useEffect } from 'react';
import { Sparkles, Loader2, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';

interface QueryInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading?: boolean;
  hasResult?: boolean;
}

export function QueryInput({
  value,
  onChange,
  onSubmit,
  isLoading,
  hasResult,
}: QueryInputProps) {
  const [isFocused, setIsFocused] = useState(false);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      onSubmit();
    }
  };

  const placeholderExamples = [
    "Show me the top 10 USDC holders on Solana...",
    "Get daily transaction volume for Jupiter DEX...",
    "Find the largest NFT sales in the last 24 hours...",
    "Analyze SOL staking rewards by validator...",
  ];

  const [placeholder, setPlaceholder] = useState(placeholderExamples[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholder((prev) => {
        const currentIndex = placeholderExamples.indexOf(prev);
        return placeholderExamples[(currentIndex + 1) % placeholderExamples.length];
      });
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className={cn(
        'relative transition-all duration-500',
        hasResult ? 'w-full' : 'w-full max-w-2xl mx-auto'
      )}
    >
      <div
        className={cn(
          'relative rounded-lg border transition-all duration-200',
          isFocused
            ? 'border-primary/50 glow-green'
            : 'border-border hover:border-muted-foreground/30'
        )}
      >
        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className={cn(
            'min-h-[120px] resize-none border-0 bg-card/50 focus-visible:ring-0 focus-visible:ring-offset-0 text-base placeholder:text-muted-foreground/50',
            hasResult && 'min-h-[80px]'
          )}
        />
        
        <div className="flex items-center justify-between px-3 py-2 border-t border-border/50 bg-muted/20">
          <p className="hidden sm:block text-xs text-muted-foreground">
            Press <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-mono">⌘</kbd>
            {' + '}
            <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-mono">Enter</kbd>
            {' to generate'}
          </p>
          
          <Button
            onClick={onSubmit}
            disabled={isLoading || !value.trim()}
            className="gap-2 solana-gradient text-primary-foreground hover:opacity-90 transition-opacity"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                Generate SQL
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
