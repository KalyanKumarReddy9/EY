import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { MobileHeader } from "@/components/MobileHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Key, User, Bell } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Settings() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [apiKeys, setApiKeys] = useState({
    iqvia: "",
    clinicalTrials: "",
    exim: "",
  });
  const { toast } = useToast();

  const handleSaveKeys = () => {
    toast({
      title: "API Keys Saved",
      description: "Your API keys have been securely stored",
    });
  };

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <MobileHeader onMenuClick={() => setSidebarOpen(true)} />
      
      <main className="flex-1 md:ml-64 pt-14 md:pt-0">
        <div className="container max-w-4xl py-4 md:py-8 px-4">
          <div className="mb-6 md:mb-8">
            <h1 className="mb-2 text-2xl md:text-3xl font-bold text-foreground">Settings</h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Manage your account and API integrations
            </p>
          </div>

          <div className="space-y-4 md:space-y-6">
            {/* Profile Settings */}
            <Card className="shadow-card">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4 md:h-5 md:w-5 text-primary flex-shrink-0" />
                  <CardTitle className="text-lg md:text-xl">Profile Settings</CardTitle>
                </div>
                <CardDescription className="text-xs md:text-sm">Update your personal information</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 md:space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name" className="text-xs md:text-sm">Full Name</Label>
                  <Input
                    id="name"
                    defaultValue="Dr. Sarah Chen"
                    className="bg-input text-sm"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-xs md:text-sm">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    defaultValue="sarah.chen@pharma.com"
                    className="bg-input text-sm"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role" className="text-xs md:text-sm">Role</Label>
                  <Input
                    id="role"
                    defaultValue="Lead Researcher"
                    className="bg-input text-sm"
                  />
                </div>
                <Button className="w-full sm:w-auto text-sm">Save Profile</Button>
              </CardContent>
            </Card>

            {/* API Keys */}
            <Card className="shadow-card">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Key className="h-4 w-4 md:h-5 md:w-5 text-primary flex-shrink-0" />
                  <CardTitle className="text-lg md:text-xl">API Keys</CardTitle>
                </div>
                <CardDescription className="text-xs md:text-sm">
                  Manage your data source API keys and integrations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 md:space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="iqvia" className="text-xs md:text-sm">IQVIA API Key</Label>
                  <Input
                    id="iqvia"
                    type="password"
                    placeholder="Enter your IQVIA API key"
                    value={apiKeys.iqvia}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, iqvia: e.target.value })
                    }
                    className="bg-input text-sm"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="clinicalTrials" className="text-xs md:text-sm">ClinicalTrials.gov API Key</Label>
                  <Input
                    id="clinicalTrials"
                    type="password"
                    placeholder="Enter your ClinicalTrials.gov API key"
                    value={apiKeys.clinicalTrials}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, clinicalTrials: e.target.value })
                    }
                    className="bg-input text-sm"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="exim" className="text-xs md:text-sm">EXIM Data API Key</Label>
                  <Input
                    id="exim"
                    type="password"
                    placeholder="Enter your EXIM API key"
                    value={apiKeys.exim}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, exim: e.target.value })
                    }
                    className="bg-input text-sm"
                  />
                </div>
                <Button onClick={handleSaveKeys} className="w-full sm:w-auto text-sm">Save API Keys</Button>
              </CardContent>
            </Card>

            {/* Notifications */}
            <Card className="shadow-card">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Bell className="h-4 w-4 md:h-5 md:w-5 text-primary flex-shrink-0" />
                  <CardTitle className="text-lg md:text-xl">Notifications</CardTitle>
                </div>
                <CardDescription className="text-xs md:text-sm">Configure your notification preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 md:space-y-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="space-y-0.5 min-w-0 flex-1">
                    <Label className="text-xs md:text-sm">Email Notifications</Label>
                    <p className="text-[10px] md:text-xs text-muted-foreground">
                      Receive email updates about your reports
                    </p>
                  </div>
                  <Switch defaultChecked className="flex-shrink-0" />
                </div>
                <div className="flex items-center justify-between gap-3">
                  <div className="space-y-0.5 min-w-0 flex-1">
                    <Label className="text-xs md:text-sm">Agent Alerts</Label>
                    <p className="text-[10px] md:text-xs text-muted-foreground">
                      Get notified when agents complete analysis
                    </p>
                  </div>
                  <Switch defaultChecked className="flex-shrink-0" />
                </div>
                <div className="flex items-center justify-between gap-3">
                  <div className="space-y-0.5 min-w-0 flex-1">
                    <Label className="text-xs md:text-sm">Dark Mode</Label>
                    <p className="text-[10px] md:text-xs text-muted-foreground">
                      Toggle dark mode theme
                    </p>
                  </div>
                  <Switch className="flex-shrink-0" />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
