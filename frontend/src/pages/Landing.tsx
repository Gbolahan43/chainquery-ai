import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, Database, Zap, Bug, Terminal, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useEffect, useState } from 'react';
import { handleGuestAccess } from '@/lib/auth';

const typingTexts = [
    { input: "Show me top 10 SOL holders", output: "SELECT wallet, balance FROM solana.accounts ORDER BY balance DESC LIMIT 10" },
    { input: "Daily DEX trading volume", output: "SELECT date_trunc('day', block_time), SUM(amount_usd) FROM dex.trades GROUP BY 1" },
    { input: "NFT sales in the last 24h", output: "SELECT * FROM nft.trades WHERE block_time > now() - interval '24' hour" },
];

function TerminalAnimation() {
    const [textIndex, setTextIndex] = useState(0);
    const [displayedInput, setDisplayedInput] = useState('');
    const [displayedOutput, setDisplayedOutput] = useState('');
    const [phase, setPhase] = useState<'typing' | 'generating' | 'output'>('typing');

    useEffect(() => {
        const current = typingTexts[textIndex];

        if (phase === 'typing') {
            if (displayedInput.length < current.input.length) {
                const timeout = setTimeout(() => {
                    setDisplayedInput(current.input.slice(0, displayedInput.length + 1));
                }, 50);
                return () => clearTimeout(timeout);
            } else {
                const timeout = setTimeout(() => setPhase('generating'), 500);
                return () => clearTimeout(timeout);
            }
        }

        if (phase === 'generating') {
            const timeout = setTimeout(() => setPhase('output'), 800);
            return () => clearTimeout(timeout);
        }

        if (phase === 'output') {
            if (displayedOutput.length < current.output.length) {
                const timeout = setTimeout(() => {
                    setDisplayedOutput(current.output.slice(0, displayedOutput.length + 2));
                }, 20);
                return () => clearTimeout(timeout);
            } else {
                const timeout = setTimeout(() => {
                    setTextIndex((prev) => (prev + 1) % typingTexts.length);
                    setDisplayedInput('');
                    setDisplayedOutput('');
                    setPhase('typing');
                }, 3000);
                return () => clearTimeout(timeout);
            }
        }
    }, [displayedInput, displayedOutput, phase, textIndex]);

    return (
        <div className="w-full max-w-2xl mx-auto">
            <div className="rounded-lg border border-border bg-card/50 backdrop-blur-sm overflow-hidden">
                {/* Terminal Header */}
                <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-muted/30">
                    <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500/80" />
                        <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                        <div className="w-3 h-3 rounded-full bg-green-500/80" />
                    </div>
                    <span className="text-xs text-muted-foreground ml-2">chainquery-ai</span>
                </div>

                {/* Terminal Body */}
                <div className="p-4 font-mono text-sm space-y-3">
                    {/* Input Line */}
                    <div className="flex items-start gap-2">
                        <span className="text-primary">❯</span>
                        <span className="text-foreground">{displayedInput}</span>
                        {phase === 'typing' && <span className="animate-pulse">▌</span>}
                    </div>

                    {/* Generating State */}
                    {phase === 'generating' && (
                        <div className="flex items-center gap-2 text-muted-foreground">
                            <div className="animate-spin h-3 w-3 border border-primary border-t-transparent rounded-full" />
                            <span className="text-xs">Generating DuneSQL...</span>
                        </div>
                    )}

                    {/* Output */}
                    {(phase === 'output' || displayedOutput) && (
                        <div className="mt-2 p-3 rounded bg-muted/50 border border-border">
                            <pre className="text-xs text-primary/90 whitespace-pre-wrap break-all">
                                {displayedOutput}
                            </pre>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

const features = [
    {
        icon: Database,
        title: 'Schema Aware',
        description: 'Understands Solana table structures and relationships for accurate query generation.',
    },
    {
        icon: Zap,
        title: 'Solana Optimized',
        description: 'Trained on thousands of Solana-specific queries for DEX, NFT, and DeFi analytics.',
    },
    {
        icon: Bug,
        title: 'Instant Debugging',
        description: 'Paste broken SQL and let our AI agent fix syntax errors and optimize performance.',
    },
];

export default function Landing() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-background">
            {/* Navigation */}
            <nav className="border-b border-border/50 backdrop-blur-sm sticky top-0 z-50 bg-background/80">
                <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2">
                        <Terminal className="h-5 w-5 text-primary" />
                        <span className="font-semibold">ChainQuery AI</span>
                    </Link>

                    <div className="flex items-center gap-4">
                        <Link to="/login">
                            <Button variant="ghost" size="sm">
                                Sign In
                            </Button>
                        </Link>
                        <Link to="/signup">
                            <Button size="sm" className="gap-1">
                                Get Started <ChevronRight className="h-4 w-4" />
                            </Button>
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="py-24 px-6">
                <div className="max-w-6xl mx-auto text-center">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium mb-6">
                        <Zap className="h-3 w-3" />
                        Powered by AI
                    </div>

                    <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
                        Turn English into{' '}
                        <span className="solana-gradient-text">Blockchain Data</span>
                    </h1>

                    <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
                        Stop struggling with Trino SQL. Ask ChainQuery to write your Dune Analytics
                        queries in seconds. Schema-aware, Solana-optimized, and ready to deploy.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
                        <Link to="/signup">
                            <Button size="lg" className="gap-2 px-8">
                                Start Querying for Free
                                <ArrowRight className="h-4 w-4" />
                            </Button>
                        </Link>
                        <Button
                            variant="outline"
                            size="lg"
                            className="gap-2"
                            onClick={() => handleGuestAccess(navigate)}
                        >
                            <Terminal className="h-4 w-4" />
                            Try Demo (No Login)
                        </Button>
                    </div>

                    {/* Terminal Animation */}
                    <TerminalAnimation />
                </div>
            </section>

            {/* Features Section */}
            <section className="py-24 px-6 border-t border-border/50">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold mb-4">Built for Solana Developers</h2>
                        <p className="text-muted-foreground max-w-xl mx-auto">
                            Everything you need to analyze on-chain data without writing complex SQL.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        {features.map((feature) => (
                            <Card key={feature.title} className="bg-card/50 border-border/50 hover:border-primary/30 transition-colors">
                                <CardContent className="p-6">
                                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                                        <feature.icon className="h-5 w-5 text-primary" />
                                    </div>
                                    <h3 className="font-semibold mb-2">{feature.title}</h3>
                                    <p className="text-sm text-muted-foreground">{feature.description}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-24 px-6 border-t border-border/50">
                <div className="max-w-2xl mx-auto text-center">
                    <h2 className="text-3xl font-bold mb-4">Ready to query smarter?</h2>
                    <p className="text-muted-foreground mb-8">
                        Join developers using ChainQuery AI to build faster analytics dashboards.
                    </p>
                    <Link to="/signup">
                        <Button size="lg" className="gap-2">
                            Create Free Account
                            <ArrowRight className="h-4 w-4" />
                        </Button>
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-border/50 py-8 px-6">
                <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Terminal className="h-4 w-4" />
                        <span className="text-sm">© 2024 ChainQuery AI</span>
                    </div>

                    <div className="flex items-center gap-6 text-sm text-muted-foreground">
                        <a href="https://github.com/Gbolahan43/chainquery-ai" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">GitHub</a>
                        <a href="https://x.com/0xexcellus" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">Twitter</a>
                        <a href="https://linkedin.com/in/abdulbasit-olanrewaju-gbolahan" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">LinkedIn</a>
                    </div>
                </div>
            </footer>
        </div>
    );
}