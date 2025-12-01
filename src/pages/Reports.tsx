import { Sidebar } from "@/components/Sidebar";
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
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      
      <main className="ml-64 flex-1">
        <div className="container max-w-7xl py-8">
          <div className="mb-8">
            <h1 className="mb-2 text-3xl font-bold text-foreground">Reports</h1>
            <p className="text-muted-foreground">
              Access and download your pharmaceutical research reports
            </p>
          </div>

          <div className="space-y-4">
            {reports.map((report) => (
              <Card key={report.id} className="shadow-card transition-all hover:shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex flex-1 items-start gap-4">
                      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10">
                        <FileText className="h-6 w-6 text-primary" />
                      </div>
                      <div className="flex-1 space-y-2">
                        <h3 className="font-semibold text-foreground">{report.title}</h3>
                        <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            {new Date(report.date).toLocaleDateString()}
                          </div>
                          <Badge variant="secondary">{report.category}</Badge>
                          <span>{report.size}</span>
                        </div>
                      </div>
                    </div>
                    <Button size="sm">
                      <Download className="mr-2 h-4 w-4" />
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
