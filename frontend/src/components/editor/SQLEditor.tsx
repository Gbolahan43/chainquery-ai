import { useRef, useCallback } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import { Copy, ExternalLink, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from '@/hooks/use-toast';
import { useState } from 'react';

interface SQLEditorProps {
  value: string;
  isLoading?: boolean;
}

export function SQLEditor({ value, isLoading }: SQLEditorProps) {
  const editorRef = useRef<any>(null);
  const [copied, setCopied] = useState(false);

  const handleEditorMount: OnMount = (editor) => {
    editorRef.current = editor;
  };

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      toast({
        title: 'Copied!',
        description: 'SQL copied to clipboard',
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast({
        title: 'Failed to copy',
        description: 'Could not copy to clipboard',
        variant: 'destructive',
      });
    }
  }, [value]);

  const handleOpenInDune = useCallback(() => {
    const duneUrl = `https://dune.com/queries/new?query=${encodeURIComponent(value)}`;
    window.open(duneUrl, '_blank', 'noopener,noreferrer');
  }, [value]);

  if (isLoading) {
    return (
      <div className="editor-container h-full">
        <div className="terminal-header">
          <div className="terminal-dot bg-destructive/70" />
          <div className="terminal-dot bg-yellow-500/70" />
          <div className="terminal-dot bg-primary/70" />
          <span className="ml-2 text-xs text-muted-foreground">Generating SQL...</span>
        </div>
        <div className="p-6 space-y-3">
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className="h-4 bg-muted/30 rounded animate-pulse"
              style={{ width: `${Math.random() * 40 + 60}%` }}
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="editor-container h-full flex flex-col">
      <div className="terminal-header justify-between">
        <div className="flex items-center gap-2">
          <div className="terminal-dot bg-destructive/70" />
          <div className="terminal-dot bg-yellow-500/70" />
          <div className="terminal-dot bg-primary/70" />
          <span className="ml-2 text-xs text-muted-foreground font-mono">
            generated.sql
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="h-7 px-2 text-xs gap-1.5 text-muted-foreground hover:text-foreground"
          >
            {copied ? (
              <>
                <Check className="h-3 w-3" />
                Copied
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                Copy
              </>
            )}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenInDune}
            className="h-7 px-2 text-xs gap-1.5 text-muted-foreground hover:text-foreground"
          >
            <ExternalLink className="h-3 w-3" />
            Open in Dune
          </Button>
        </div>
      </div>
      
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          language="sql"
          theme="vs-dark"
          value={value}
          onMount={handleEditorMount}
          options={{
            readOnly: true,
            minimap: { enabled: false },
            fontSize: 13,
            fontFamily: "'JetBrains Mono', monospace",
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            padding: { top: 16, bottom: 16 },
            renderLineHighlight: 'none',
            overviewRulerBorder: false,
            hideCursorInOverviewRuler: true,
            scrollbar: {
              vertical: 'auto',
              horizontal: 'auto',
              verticalScrollbarSize: 8,
              horizontalScrollbarSize: 8,
            },
          }}
        />
      </div>
    </div>
  );
}
