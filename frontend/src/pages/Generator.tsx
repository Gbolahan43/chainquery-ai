import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { AlertCircle, Database, Zap } from 'lucide-react';
import { QueryInput } from '@/components/query/QueryInput';
import { SQLEditor } from '@/components/editor/SQLEditor';
import { useGenerateSQL } from '@/hooks/useChainQuery';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { LayoutContext } from '@/components/layout/Layout';
import { cn } from '@/lib/utils';

export default function Generator() {
  const { selectedSQL, selectedInput, setSelectedQuery } = useOutletContext<LayoutContext>();
  const [input, setInput] = useState('');
  const [generatedSQL, setGeneratedSQL] = useState('');

  const generateMutation = useGenerateSQL();

  // Handle selected query from history OR clear when New Query is clicked
  useEffect(() => {
    if (selectedInput) {
      setInput(selectedInput);
    } else {
      setInput('');
    }
    if (selectedSQL) {
      setGeneratedSQL(selectedSQL);
    } else {
      setGeneratedSQL('');
    }
  }, [selectedInput, selectedSQL]);

  const handleGenerate = async () => {
    if (!input.trim()) return;

    try {
      const result = await generateMutation.mutateAsync({
        user_input: input,
        chain: 'solana',
      });

      if (result.error_message) {
        throw new Error(result.error_message);
      }

      setGeneratedSQL(result.sql_output);
    } catch (error) {
      // Error handling is done via the mutation
    }
  };

  const hasResult = generatedSQL.length > 0 || generateMutation.isPending;

  return (
    <div className="h-full flex flex-col">
      {/* Hero Section - only show when no result */}
      {!hasResult && (
        <div className="flex-1 flex flex-col items-center justify-center px-6 py-12">
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium mb-4">
              <Zap className="h-3 w-3" />
              AI-Powered SQL Generation
            </div>
            <h1 className="text-3xl md:text-4xl font-bold mb-3">
              Query Solana with{' '}
              <span className="solana-gradient-text">Natural Language</span>
            </h1>
            <p className="text-muted-foreground max-w-lg mx-auto">
              Describe what you want to analyze, and our AI will generate
              production-ready DuneSQL queries for Solana blockchain data.
            </p>
          </div>

          <QueryInput
            value={input}
            onChange={setInput}
            onSubmit={handleGenerate}
            isLoading={generateMutation.isPending}
            hasResult={hasResult}
          />

          {/* Example Queries */}
          <div className="mt-8 flex flex-wrap justify-center gap-2">
            {[
              'Top 10 SOL holders',
              'Daily DEX volume',
              'NFT sales today',
              'Token transfers',
            ].map((example) => (
              <button
                key={example}
                onClick={() => setInput(example)}
                className="px-3 py-1.5 rounded-full text-xs border border-border text-muted-foreground hover:text-foreground hover:border-muted-foreground transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Split View - show when there's a result */}
      {hasResult && (
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Input Section - Compact */}
          <div className="p-4 border-b border-border bg-card/30">
            <QueryInput
              value={input}
              onChange={setInput}
              onSubmit={handleGenerate}
              isLoading={generateMutation.isPending}
              hasResult={hasResult}
            />
          </div>

          {/* Error Alert */}
          {generateMutation.isError && (
            <Alert variant="destructive" className="mx-4 mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                {generateMutation.error?.message || 'Failed to generate SQL. Please try again.'}
              </AlertDescription>
            </Alert>
          )}

          {/* Editor Section */}
          <div className="flex-1 p-4 overflow-hidden">
            <SQLEditor
              value={generatedSQL}
              isLoading={generateMutation.isPending}
            />
          </div>
        </div>
      )}
    </div>
  );
}
