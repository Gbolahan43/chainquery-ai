import { Wrench, Bell, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function Debug() {
  return (
    <div className="h-full flex items-center justify-center p-6">
      <Card className="w-full max-w-md border-border/50 bg-card/50 backdrop-blur-sm">
        <CardContent className="pt-8 pb-8 text-center">
          {/* Icon */}
          <div className="relative mx-auto mb-6 w-fit">
            <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-muted/50 border border-border">
              <Wrench className="h-10 w-10 text-muted-foreground" />
            </div>
            <div className="absolute -right-2 -top-2">
              <Badge variant="secondary" className="gap-1 text-[10px] px-2 py-0.5">
                <Lock className="h-2.5 w-2.5" />
                v2.0
              </Badge>
            </div>
          </div>

          {/* Title */}
          <h2 className="text-xl font-semibold mb-2">AI SQL Debugger</h2>
          
          {/* Description */}
          <p className="text-muted-foreground text-sm mb-6 max-w-xs mx-auto">
            Paste your broken SQL and let our Agent analyze, explain, and fix it automatically.
            Coming in version 2.0.
          </p>

          {/* Features Preview */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            {['Error Detection', 'Auto-Fix', 'Explanations'].map((feature) => (
              <div
                key={feature}
                className="p-2 rounded-md bg-muted/30 border border-border/50"
              >
                <span className="text-xs text-muted-foreground">{feature}</span>
              </div>
            ))}
          </div>

          {/* CTA */}
          <Button
            variant="outline"
            className="gap-2 cursor-not-allowed opacity-60"
            disabled
          >
            <Bell className="h-4 w-4" />
            Notify Me
          </Button>
          
          <p className="text-[10px] text-muted-foreground mt-3">
            We'll email you when debugging is available
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
