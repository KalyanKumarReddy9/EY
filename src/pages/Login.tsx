import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Database } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Login() {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simple demo login - in production, connect to Lovable Cloud auth
    toast({
      title: isSignup ? "Account Created" : "Welcome Back",
      description: `Successfully ${isSignup ? "signed up" : "logged in"} as ${email}`,
    });
    navigate("/dashboard");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="mb-6 md:mb-8 text-center">
          <div className="mx-auto mb-3 md:mb-4 flex h-12 w-12 md:h-16 md:w-16 items-center justify-center rounded-2xl bg-primary">
            <Database className="h-6 w-6 md:h-8 md:w-8 text-primary-foreground" />
          </div>
          <h1 className="text-xl md:text-2xl font-bold text-foreground">Pharma AI Research</h1>
          <p className="mt-1 text-xs md:text-sm text-muted-foreground">
            AI-Powered Analytics Platform
          </p>
        </div>

        <Card className="shadow-card">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-xl md:text-2xl font-semibold">
              {isSignup ? "Create Account" : "Welcome Back"}
            </CardTitle>
            <CardDescription className="text-xs md:text-sm">
              {isSignup
                ? "Enter your details to create your account"
                : "Enter your credentials to access your dashboard"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-3 md:space-y-4">
              {isSignup && (
                <div className="space-y-2">
                  <Label htmlFor="name" className="text-xs md:text-sm">Full Name</Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Dr. Sarah Chen"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    className="bg-input text-sm"
                  />
                </div>
              )}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-xs md:text-sm">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="sarah.chen@pharma.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="bg-input text-sm"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password" className="text-xs md:text-sm">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="bg-input text-sm"
                />
              </div>
              {isSignup && (
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword" className="text-xs md:text-sm">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="••••••••"
                    required
                    className="bg-input text-sm"
                  />
                </div>
              )}
              <Button type="submit" className="w-full text-sm md:text-base" size="lg">
                {isSignup ? "Create Account" : "Sign In"}
              </Button>
            </form>

            <div className="mt-4 md:mt-6 text-center">
              <button
                type="button"
                onClick={() => setIsSignup(!isSignup)}
                className="text-xs md:text-sm text-muted-foreground hover:text-primary transition-colors"
              >
                {isSignup
                  ? "Already have an account? Sign in"
                  : "Don't have an account? Sign up"}
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
