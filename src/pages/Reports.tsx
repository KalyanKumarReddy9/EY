import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Calendar } from "lucide-react";

const reports = [
  {
    id: 1,
    title: "Diabetes Therapeutics Market Analysis",
    date: "2025-11-28",
    category: "Market Research",
    status: "completed",
    size: "2.4 MB",
  },
  {
    id: 2,
    title: "Global Oncology Trade Flow Report Q4 2025",
    date: "2025-11-25",
    category: "Trade Data",
    status: "completed",
    size: "3.1 MB",
  },
  {
    id: 3,
    title: "Phase III Clinical Trials Pipeline Update",
    date: "2025-11-20",
    category: "Clinical Trials",
    status: "completed",
    size: "1.8 MB",
  },
  {
    id: 4,
    title: "Cardiovascular Drug Market Forecast 2026",
    date: "2025-11-15",
    category: "Market Research",
    status: "completed",
    size: "2.9 MB",
  },
];

export default function Reports() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

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

          <div className="space-y-3 md:space-y-4">
            {reports.map((report) => (
              <Card key={report.id} className="shadow-card transition-all hover:shadow-lg">
                <CardContent className="p-4 md:p-6">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 md:gap-4">
                    <div className="flex flex-1 items-start gap-3 md:gap-4 min-w-0 w-full sm:w-auto">
                      <div className="flex h-10 w-10 md:h-12 md:w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10">
                        <FileText className="h-5 w-5 md:h-6 md:w-6 text-primary" />
                      </div>
                      <div className="flex-1 space-y-1 md:space-y-2 min-w-0">
                        <h3 className="font-semibold text-sm md:text-base text-foreground truncate">{report.title}</h3>
                        <div className="flex flex-wrap items-center gap-2 md:gap-3 text-xs md:text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3 md:h-4 md:w-4 flex-shrink-0" />
                            {new Date(report.date).toLocaleDateString()}
                          </div>
                          <Badge variant="secondary" className="text-[10px] md:text-xs">{report.category}</Badge>
                          <span className="text-[10px] md:text-xs">{report.size}</span>
                        </div>
                      </div>
                    </div>
                    <Button size="sm" className="w-full sm:w-auto text-xs md:text-sm">
                      <Download className="mr-2 h-3.5 w-3.5 md:h-4 md:w-4" />
                      Download
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
