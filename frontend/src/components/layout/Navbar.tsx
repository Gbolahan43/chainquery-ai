import { Badge } from '@/components/ui/badge';
import { Circle } from 'lucide-react';
import { UserMenu } from './UserMenu';

export function Navbar() {
  return (
    <nav className="h-14 border-b border-border flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <h1 className="text-sm font-medium text-muted-foreground">
          SQL Generator
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <Badge
          variant="outline"
          className="gap-1.5 px-3 py-1 border-primary/30 text-primary bg-primary/5"
        >
          <Circle className="h-2 w-2 fill-primary text-primary animate-pulse" />
          Solana
        </Badge>

        <UserMenu />
      </div>
    </nav>
  );
}
