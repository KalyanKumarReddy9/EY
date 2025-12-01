import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Database, Activity, Play } from "lucide-react";

const agents = [
  {
    id: 1,
    name: "Market Insights Agent",
    source: "IQVIA",
    description: "Analyzes global pharmaceutical market data, competitive intelligence, and sales trends across therapeutic areas.",
    capabilities: ["Sales Analytics", "Market Forecasting", "Competitive Analysis"],
    status: "active",
    icon: TrendingUp,
  },
  {
    id: 2,
    name: "Trade Data Agent",
    source: "EXIM",
    description: "Monitors international pharmaceutical trade flows, import/export patterns, and supply chain dynamics.",
    capabilities: ["Trade Flow Analysis", "Supply Chain Mapping", "Import/Export Tracking"],
    status: "active",
    icon: Database,
  },
  {
    id: 3,
    name: "Clinical Trials Agent",
    source: "ClinicalTrials.gov",
    description: "Tracks ongoing clinical trials, research outcomes, and drug development pipelines worldwide.",
    capabilities: ["Trial Monitoring", "Pipeline Analysis", "Outcome Tracking"],
    status: "active",
    icon: Activity,
  },
];

export default function Agents() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex-1 md:ml-64 pt-14 md:pt-0">
        <div className="container max-w-7xl py-4 md:py-8 px-4">
          <div className="mb-4 md:mb-8">
            <h1 className="mb-1 md:mb-2 text-2xl md:text-3xl font-bold text-foreground">Worker Agents</h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Manage and monitor your AI-powered research agents
            </p>
          </div>

          <div className="grid gap-4 md:gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.id} className="shadow-card transition-all hover:shadow-lg">
                <CardHeader className="pb-3">
                  <div className="mb-2 md:mb-3 flex items-start justify-between">
                    <div className="flex h-10 w-10 md:h-12 md:w-12 items-center justify-center rounded-xl bg-primary/10">
                      <agent.icon className="h-5 w-5 md:h-6 md:w-6 text-primary" />
                    </div>
                    <Badge variant="secondary" className="bg-primary/10 text-primary text-xs">
                      {agent.status}
                    </Badge>
                  </div>
                  <CardTitle className="text-base md:text-lg">{agent.name}</CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    Source: {agent.source}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3 md:space-y-4">
                  <p className="text-xs md:text-sm leading-relaxed text-muted-foreground">
                    {agent.description}
                  </p>
                  
                  <div className="space-y-2">
                    <p className="text-xs font-medium text-foreground">Capabilities:</p>
                    <div className="flex flex-wrap gap-1.5 md:gap-2">
                      {agent.capabilities.map((capability) => (
                        <Badge
                          key={capability}
                          variant="outline"
                          className="text-[10px] md:text-xs"
                        >
                          {capability}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <Button className="w-full" size="sm">
                    <Play className="mr-2 h-3.5 w-3.5 md:h-4 md:w-4" />
                    <span className="text-xs md:text-sm">Start Analysis</span>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
