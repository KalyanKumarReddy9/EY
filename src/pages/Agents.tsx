import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Database, Activity, Play } from "lucide-react";

export const agents = [
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
  {
    id: 4,
    name: "Patent & IP Agent",
    source: "USPTO + EPO",
    description: "Scans patent filings, intellectual property landscapes, and freedom-to-operate risks for drug compounds.",
    capabilities: ["Patent Landscaping", "FTO Analysis", "IP Monitoring"],
    status: "active",
    icon: Database,
  },
  {
    id: 5,
    name: "Safety Signal Agent",
    source: "FAERS / EudraVigilance",
    description: "Detects emerging safety signals, adverse events, and pharmacovigilance trends from global reporting systems.",
    capabilities: ["AE Detection", "Signal Prioritization", "Regulatory Alerts"],
    status: "active",
    icon: Activity,
  },
  {
    id: 6,
    name: "Regulatory Monitor Agent",
    source: "WHO / EMA / FDA",
    description: "Keeps track of regulatory guidance, labeling changes, and compliance updates across regions.",
    capabilities: ["Guidance Tracking", "Label Change Alerts", "Compliance Summaries"],
    status: "active",
    icon: TrendingUp,
  },
  {
    id: 7,
    name: "Supply Chain Risk Agent",
    source: "Global Trade + Supplier Feeds",
    description: "Analyzes supplier risk, raw material shortages, and distribution disruptions affecting drug availability.",
    capabilities: ["Risk Scoring", "Supplier Profiling", "Alternative Sourcing"],
    status: "active",
    icon: Database,
  },
  {
    id: 8,
    name: "Clinical Evidence Summarizer",
    source: "Literature & Internal Docs",
    description: "Ingests clinical papers, internal study reports and summarizes evidence for quick review by medical teams.",
    capabilities: ["Evidence Extraction", "Summary Generation", "Citation Linking"],
    status: "active",
    icon: Activity,
  },
];

export default function Agents() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  const handleStartAnalysis = () => {
    // Navigate to the chat page when "Start Analysis" is clicked
    navigate("/chat");
  };

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

          <div className="grid gap-5 md:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.id} className="card-elevated border-border/50 hover:border-primary/30 hover:shadow-xl transition-all duration-300 group flex flex-col h-full">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-primary/10 group-hover:from-primary/30 group-hover:to-primary/15 transition-all duration-300">
                      <agent.icon className="h-6 w-6 text-primary" />
                    </div>
                    <Badge variant="secondary" className="bg-primary/10 text-primary text-xs font-medium px-2.5 py-1">
                      {agent.status}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg font-bold mb-1.5">{agent.name}</CardTitle>
                  <CardDescription className="text-xs text-muted-foreground font-medium">
                    {agent.source}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col pt-0">
                  <div className="flex-1 space-y-4">
                    <p className="text-sm leading-relaxed text-muted-foreground min-h-[4rem]">
                      {agent.description}
                    </p>
                    
                    <div>
                      <p className="text-xs font-semibold text-foreground mb-2">Key Capabilities</p>
                      <div className="flex flex-wrap gap-2 min-h-[3.5rem]">
                        {agent.capabilities.map((capability) => (
                          <Badge
                            key={capability}
                            variant="outline"
                            className="text-xs font-medium border-primary/30 hover:bg-primary/5 transition-colors"
                          >
                            {capability}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  <Button 
                    onClick={handleStartAnalysis}
                    className="w-full mt-4 bg-gradient-medical hover:opacity-90 hover:scale-[1.02] transition-all group-hover:shadow-lg font-medium" 
                    size="default"
                  >
                    <Play className="mr-2 h-4 w-4" />
                    Start Analysis
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