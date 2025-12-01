import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Key, User, Bell } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Settings() {
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
      <Sidebar />
      
      <main className="ml-64 flex-1">
        <div className="container max-w-4xl py-8">
          <div className="mb-8">
            <h1 className="mb-2 text-3xl font-bold text-foreground">Settings</h1>
            <p className="text-muted-foreground">
              Manage your account and API integrations
            </p>
          </div>

          <div className="space-y-6">
            {/* Profile Settings */}
            <Card className="shadow-card">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <User className="h-5 w-5 text-primary" />
                  <CardTitle>Profile Settings</CardTitle>
                </div>
                <CardDescription>Update your personal information</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    defaultValue="Dr. Sarah Chen"
                    className="bg-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    defaultValue="sarah.chen@pharma.com"
                    className="bg-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role">Role</Label>
                  <Input
                    id="role"
                    defaultValue="Lead Researcher"
                    className="bg-input"
                  />
                </div>
                <Button>Save Profile</Button>
              </CardContent>
            </Card>

            {/* API Keys */}
            <Card className="shadow-card">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Key className="h-5 w-5 text-primary" />
                  <CardTitle>API Keys</CardTitle>
                </div>
                <CardDescription>
                  Manage your data source API keys and integrations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="iqvia">IQVIA API Key</Label>
                  <Input
                    id="iqvia"
                    type="password"
                    placeholder="Enter your IQVIA API key"
                    value={apiKeys.iqvia}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, iqvia: e.target.value })
                    }
                    className="bg-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="clinicalTrials">ClinicalTrials.gov API Key</Label>
                  <Input
                    id="clinicalTrials"
                    type="password"
                    placeholder="Enter your ClinicalTrials.gov API key"
                    value={apiKeys.clinicalTrials}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, clinicalTrials: e.target.value })
                    }
                    className="bg-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="exim">EXIM Data API Key</Label>
                  <Input
                    id="exim"
                    type="password"
                    placeholder="Enter your EXIM API key"
                    value={apiKeys.exim}
                    onChange={(e) =>
                      setApiKeys({ ...apiKeys, exim: e.target.value })
                    }
                    className="bg-input"
                  />
                </div>
                <Button onClick={handleSaveKeys}>Save API Keys</Button>
              </CardContent>
            </Card>

            {/* Notifications */}
            <Card className="shadow-card">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Bell className="h-5 w-5 text-primary" />
                  <CardTitle>Notifications</CardTitle>
                </div>
                <CardDescription>Configure your notification preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Email Notifications</Label>
                    <p className="text-sm text-muted-foreground">
                      Receive email updates about your reports
                    </p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Agent Alerts</Label>
                    <p className="text-sm text-muted-foreground">
                      Get notified when agents complete analysis
                    </p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Dark Mode</Label>
                    <p className="text-sm text-muted-foreground">
                      Toggle dark mode theme
                    </p>
                  </div>
                  <Switch />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
