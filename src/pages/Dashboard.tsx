import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
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
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex-1 md:ml-64 pt-14 md:pt-0">
        <div className="container max-w-7xl py-4 md:py-8 px-4">
          {/* Hero Section */}
          <div className="mb-6 md:mb-8">
            <h1 className="mb-2 text-2xl md:text-3xl font-bold text-foreground">
              Welcome back, Dr. Chen
            </h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Your AI-powered pharmaceutical research dashboard
            </p>
          </div>

          {/* Agent Cards */}
          <div className="mb-8 md:mb-12 grid gap-4 md:gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.name} className="shadow-card transition-all hover:shadow-lg">
                <CardHeader className="pb-3">
                  <div className="mb-2 md:mb-3 flex h-10 w-10 md:h-12 md:w-12 items-center justify-center rounded-xl bg-primary/10">
                    <agent.icon className="h-5 w-5 md:h-6 md:w-6 text-primary" />
                  </div>
                  <CardTitle className="text-base md:text-lg">{agent.name}</CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    {agent.source}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3 md:space-y-4">
                  <p className="text-xs md:text-sm text-muted-foreground leading-relaxed">
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
                          <div className="h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                          {capability}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <Button className="w-full text-sm" size="sm">
                    Start Analysis <ArrowRight className="ml-2 h-3.5 w-3.5 md:h-4 md:w-4" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* How It Works */}
          <Card className="shadow-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg md:text-xl">How It Works</CardTitle>
              <CardDescription className="text-xs md:text-sm">
                Three simple steps to unlock powerful pharmaceutical insights
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:gap-8 sm:grid-cols-2 lg:grid-cols-3">
                {processSteps.map((step, index) => (
                  <div key={step.step} className="relative">
                    <div className="mb-3 md:mb-4 flex items-center gap-3 md:gap-4">
                      <div className="flex h-10 w-10 md:h-12 md:w-12 shrink-0 items-center justify-center rounded-full bg-primary text-base md:text-lg font-bold text-primary-foreground">
                        {step.step}
                      </div>
                      {index < processSteps.length - 1 && (
                        <div className="hidden h-0.5 flex-1 bg-border lg:block" />
                      )}
                    </div>
                    <h3 className="mb-2 font-semibold text-sm md:text-base text-foreground">{step.title}</h3>
                    <p className="text-xs md:text-sm text-muted-foreground">{step.description}</p>
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
