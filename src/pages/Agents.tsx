import { Sidebar } from "@/components/Sidebar";
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
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      
      <main className="ml-64 flex-1">
        <div className="container max-w-7xl py-8">
          <div className="mb-8">
            <h1 className="mb-2 text-3xl font-bold text-foreground">Worker Agents</h1>
            <p className="text-muted-foreground">
              Manage and monitor your AI-powered research agents
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.id} className="shadow-card transition-all hover:shadow-lg">
                <CardHeader>
                  <div className="mb-3 flex items-start justify-between">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                      <agent.icon className="h-6 w-6 text-primary" />
                    </div>
                    <Badge variant="secondary" className="bg-primary/10 text-primary">
                      {agent.status}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg">{agent.name}</CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    Source: {agent.source}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {agent.description}
                  </p>
                  
                  <div className="space-y-2">
                    <p className="text-xs font-medium text-foreground">Capabilities:</p>
                    <div className="flex flex-wrap gap-2">
                      {agent.capabilities.map((capability) => (
                        <Badge
                          key={capability}
                          variant="outline"
                          className="text-xs"
                        >
                          {capability}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <Button className="w-full" size="sm">
                    <Play className="mr-2 h-4 w-4" />
                    Start Analysis with This Agent
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
