import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { FileText, Search, Download, Calendar, Filter } from "lucide-react";
import { agents } from "./Agents";

interface Report {
  id: string;
  title: string;
  agent: string;
  date: string;
  size: string;
}

export default function Reports() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedAgent, setSelectedAgent] = useState<string>("all");
  const [sortBy, setSortBy] = useState<string>("date");
  
  // Empty reports array - will be populated when agents generate reports
  const [reports] = useState<Report[]>([]);

  // Get all agent names from the agents array
  const agentNames = agents.map((agent) => agent.name).sort();

  // Filter and sort reports
  const filteredReports = reports
    .filter((report) => {
      const matchesSearch = report.title.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesAgent = selectedAgent === "all" || report.agent === selectedAgent;
      return matchesSearch && matchesAgent;
    })
    .sort((a, b) => {
      if (sortBy === "date") {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      } else if (sortBy === "name") {
        return a.title.localeCompare(b.title);
      }
      return 0;
    });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex-1 md:ml-64 pt-14 md:pt-0">
        <div className="container max-w-7xl py-4 md:py-8 px-4">
          <div className="mb-6 md:mb-8">
            <h1 className="mb-2 text-2xl md:text-3xl font-bold text-foreground">Reports</h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Access and download your pharmaceutical research reports
            </p>
          </div>

          {/* Search and Filters */}
          <div className="mb-6 space-y-3">
            <div className="grid gap-3 md:grid-cols-3">
              {/* Search by Name */}
              <div className="relative md:col-span-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search by report name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-input text-sm"
                />
              </div>

              {/* Filter by Agent */}
              <div className="relative">
                <Select value={selectedAgent} onValueChange={setSelectedAgent}>
                  <SelectTrigger className="bg-input text-sm">
                    <div className="flex items-center gap-2">
                      <Filter className="h-4 w-4 text-muted-foreground" />
                      <SelectValue placeholder="Filter by agent" />
                    </div>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Agents</SelectItem>
                    {agentNames.map((agentName) => (
                      <SelectItem key={agentName} value={agentName}>
                        {agentName}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Sort By */}
              <div className="relative">
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="bg-input text-sm">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="date">Sort by Date (Newest)</SelectItem>
                    <SelectItem value="name">Sort by Name (A-Z)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Active Filters Display */}
            {(selectedAgent !== "all" || searchQuery) && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span>Active filters:</span>
                {searchQuery && (
                  <span className="bg-primary/10 text-primary px-2 py-1 rounded">
                    Name: "{searchQuery}"
                  </span>
                )}
                {selectedAgent !== "all" && (
                  <span className="bg-primary/10 text-primary px-2 py-1 rounded">
                    Agent: {selectedAgent}
                  </span>
                )}
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedAgent("all");
                  }}
                  className="text-primary hover:underline ml-2"
                >
                  Clear all
                </button>
              </div>
            )}
          </div>

          {/* Reports List */}
          {filteredReports.length > 0 ? (
            <div className="grid gap-4 md:gap-5">
              {filteredReports.map((report) => (
                <Card key={report.id} className="shadow-card border-border/50 hover:shadow-lg transition-all duration-300 group">
                  <CardContent className="p-4 md:p-5">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3 md:gap-4 flex-1 min-w-0">
                        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-primary/10 flex-shrink-0">
                          <FileText className="h-6 w-6 text-primary" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="text-base md:text-lg font-semibold text-foreground mb-1 truncate">
                            {report.title}
                          </h3>
                          <div className="flex flex-wrap items-center gap-3 text-xs md:text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Calendar className="h-3.5 w-3.5" />
                              {formatDate(report.date)}
                            </span>
                            <span>•</span>
                            <span>{report.agent}</span>
                            <span>•</span>
                            <span>{report.size}</span>
                          </div>
                        </div>
                      </div>
                      <Button
                        size="sm"
                        className="flex-shrink-0 bg-gradient-medical hover:opacity-90 transition-all group-hover:scale-105"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Download
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="shadow-card border-border/50">
              <CardHeader className="text-center py-12 md:py-16">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/10 to-primary/5">
                  <FileText className="h-8 w-8 text-primary" />
                </div>
                <CardTitle className="text-xl md:text-2xl">No Reports Found</CardTitle>
                <CardDescription className="text-sm md:text-base mt-2">
                  {searchQuery ? `No reports match "${searchQuery}"` : "Your generated reports will appear here once you run analyses with the AI agents"}
                </CardDescription>
              </CardHeader>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
