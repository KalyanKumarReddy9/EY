import { Sidebar } from "@/components/Sidebar";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TrendingUp, Database, Activity, ArrowRight } from "lucide-react";

const agents = [
  {
    name: "Market Insights Agent",
    source: "IQVIA",
    description: "Analyzes global pharmaceutical market data, competitive intelligence, and sales trends across therapeutic areas.",
    capabilities: ["Sales Analytics", "Market Forecasting", "Competitive Analysis"],
    icon: TrendingUp,
  },
  {
    name: "Trade Data Agent",
    source: "EXIM",
    description: "Monitors international pharmaceutical trade flows, import/export patterns, and supply chain dynamics.",
    capabilities: ["Trade Flow Analysis", "Supply Chain Mapping", "Import/Export Tracking"],
    icon: Database,
  },
  {
    name: "Clinical Trials Agent",
    source: "ClinicalTrials.gov",
    description: "Tracks ongoing clinical trials, research outcomes, and drug development pipelines worldwide.",
    capabilities: ["Trial Monitoring", "Pipeline Analysis", "Outcome Tracking"],
    icon: Activity,
  },
];

const processSteps = [
  {
    step: 1,
    title: "Connect Data Sources",
    description: "Integrate your pharmaceutical databases and research platforms",
  },
  {
    step: 2,
    title: "AI Analysis",
    description: "Our agents analyze data using advanced machine learning models",
  },
  {
    step: 3,
    title: "Actionable Insights",
    description: "Receive comprehensive reports with strategic recommendations",
  },
];

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      
      <main className="ml-64 flex-1">
        <div className="container max-w-7xl py-8">
          {/* Hero Section */}
          <div className="mb-8">
            <h1 className="mb-2 text-3xl font-bold text-foreground">
              Welcome back, Dr. Chen
            </h1>
            <p className="text-muted-foreground">
              Your AI-powered pharmaceutical research dashboard
            </p>
          </div>

          {/* Agent Cards */}
          <div className="mb-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.name} className="shadow-card transition-all hover:shadow-lg">
                <CardHeader>
                  <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                    <agent.icon className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{agent.name}</CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    {agent.source}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {agent.description}
                  </p>
                  <div className="space-y-2">
                    <p className="text-xs font-medium text-foreground">Key Capabilities:</p>
                    <ul className="space-y-1">
                      {agent.capabilities.map((capability) => (
                        <li
                          key={capability}
                          className="text-xs text-muted-foreground flex items-center gap-2"
                        >
                          <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                          {capability}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <Button className="w-full" size="sm">
                    Start Analysis <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* How It Works */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>How It Works</CardTitle>
              <CardDescription>
                Three simple steps to unlock powerful pharmaceutical insights
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-8 md:grid-cols-3">
                {processSteps.map((step, index) => (
                  <div key={step.step} className="relative">
                    <div className="mb-4 flex items-center gap-4">
                      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                        {step.step}
                      </div>
                      {index < processSteps.length - 1 && (
                        <div className="hidden h-0.5 flex-1 bg-border md:block" />
                      )}
                    </div>
                    <h3 className="mb-2 font-semibold text-foreground">{step.title}</h3>
                    <p className="text-sm text-muted-foreground">{step.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
