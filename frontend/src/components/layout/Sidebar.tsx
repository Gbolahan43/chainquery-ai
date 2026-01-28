import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Terminal,
  Plus,
  Github,
  Twitter,
  Linkedin,
  History,
  ChevronLeft,
  ChevronRight,
  Database,
  Sparkles,
  Bug,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useHistory } from '@/hooks/useChainQuery';
import { cn } from '@/lib/utils';
import { NavLink } from '@/components/NavLink';

interface SidebarProps {
  onSelectQuery?: (sql: string, input: string) => void;
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ onSelectQuery, collapsed, onToggle }: SidebarProps) {
  const { data: history, isLoading } = useHistory();
  const navigate = useNavigate();
  const location = useLocation();

  const handleNewChat = () => {
    navigate('/dashboard');
    onSelectQuery?.('', '');
  };

  const handleHistoryClick = (item: { user_input: string; sql_output?: string }) => {
    navigate('/dashboard');
    onSelectQuery?.(item.sql_output || '', item.user_input);
  };

  const truncateText = (text: string, maxLength: number = 28) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + '...';
  };

  return (
    <aside
      className={cn(
        'h-screen glass flex flex-col transition-all duration-300 ease-in-out relative',
        collapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="absolute -right-3 top-6 z-50 flex h-6 w-6 items-center justify-center rounded-full border border-border bg-card hover:bg-muted transition-colors"
      >
        {collapsed ? (
          <ChevronRight className="h-3 w-3 text-muted-foreground" />
        ) : (
          <ChevronLeft className="h-3 w-3 text-muted-foreground" />
        )}
      </button>

      {/* Header */}
      <div className="flex items-center gap-3 p-4 border-b border-border">
        <div className="flex h-9 w-9 items-center justify-center rounded-md solana-gradient">
          <Terminal className="h-5 w-5 text-primary-foreground" />
        </div>
        {!collapsed && (
          <div className="flex flex-col">
            <span className="font-semibold text-sm">ChainQuery</span>
            <span className="text-xs text-muted-foreground">AI SQL Generator</span>
          </div>
        )}
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <Button
          onClick={handleNewChat}
          variant="outline"
          className={cn(
            'w-full justify-start gap-2 border-dashed hover:border-primary hover:text-primary transition-colors',
            collapsed && 'justify-center px-2'
          )}
        >
          <Plus className="h-4 w-4" />
          {!collapsed && <span>New Query</span>}
        </Button>
      </div>

      {/* History Section */}
      {!collapsed && (
        <div className="px-3 py-2">
          <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
            <History className="h-3 w-3" />
            <span>Query History</span>
          </div>
        </div>
      )}

      {/* History List */}
      <ScrollArea className="flex-1 px-3">
        {isLoading ? (
          <div className="space-y-2 py-2">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="h-10 rounded-md bg-muted/50 animate-pulse"
              />
            ))}
          </div>
        ) : history && history.length > 0 ? (
          <div className="space-y-1 py-2">
            {history.map((item) => (
              <button
                key={item.id}
                onClick={() => handleHistoryClick(item)}
                className={cn(
                  'w-full text-left px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors flex items-center gap-2',
                  collapsed && 'justify-center px-2'
                )}
              >
                <Database className="h-3 w-3 shrink-0" />
                {!collapsed && (
                  <span className="truncate">
                    {truncateText(item.user_input)}
                  </span>
                )}
              </button>
            ))}
          </div>
        ) : !collapsed ? (
          <div className="py-8 text-center">
            <Sparkles className="h-8 w-8 mx-auto text-muted-foreground/50 mb-2" />
            <p className="text-xs text-muted-foreground">
              No queries yet
            </p>
          </div>
        ) : null}
      </ScrollArea>

      {/* Nav Links */}
      <div className="px-3 py-2 border-t border-border">
        <NavLink
          to="/debug"
          className={cn(
            'w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors',
            collapsed && 'justify-center px-2'
          )}
          activeClassName="bg-muted/50 text-foreground"
        >
          <Bug className="h-4 w-4 shrink-0" />
          {!collapsed && <span>SQL Debugger</span>}
        </NavLink>
      </div>

      {/* Footer Links */}
      <div className={cn(
        'p-3 border-t border-border flex gap-2',
        collapsed ? 'flex-col items-center' : 'items-center'
      )}>
        <a
          href="https://github.com/Gbolahan43"
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
        >
          <Github className="h-4 w-4" />
        </a>
        <a
          href="https://x.com/0xexcellus"
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
        >
          <Twitter className="h-4 w-4" />
        </a>
        <a
          href="https://linkedin.com/in/abdulbasit-olanrewaju-gbolahan"
          target="_blank"
          rel="noopener noreferrer"
          className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
        >
          <Linkedin className="h-4 w-4" />
        </a>
      </div>
    </aside>
  );
}
