import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Database, ArrowLeft, User } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Login() {
  const [isSignup, setIsSignup] = useState(false);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();
  const API = (import.meta.env && import.meta.env.VITE_API_URL) || 'http://localhost:4000';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isForgotPassword) {
      toast({
        title: "Reset Link Sent",
        description: `Password reset instructions have been sent to ${email}`,
      });
      setIsForgotPassword(false);
      return;
    }
    // Call backend auth
    const url = `${API}/api/auth/${isSignup ? 'signup' : 'signin'}`;
    const body: any = { email, password };
    if (isSignup) { body.name = name; body.role = role; }
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.msg || 'Auth failed');
        // store token and user
        if (data.token) localStorage.setItem('token', data.token);
        if (data.user) localStorage.setItem('user', JSON.stringify(data.user));
        toast({ title: isSignup ? 'Account Created' : 'Welcome Back', description: `${isSignup ? 'Signed up' : 'Logged in'} as ${data.user.email}` });
        navigate('/dashboard');
      })
      .catch((err) => {
        toast({ title: 'Authentication Error', description: err.message || 'Unable to authenticate' });
      });
  };

  const handleToggleSignup = () => {
    setIsSignup(!isSignup);
  };

  if (isForgotPassword) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <div className="w-full max-w-md">
          {/* Logo */}
          <div className="mb-6 md:mb-8 text-center">
            <div className="mx-auto mb-3 md:mb-4 flex h-12 w-12 md:h-16 md:w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary/80 shadow-lg transform transition-transform hover:scale-110">
              <Database className="h-6 w-6 md:h-8 md:w-8 text-primary-foreground" />
            </div>
            <h1 className="text-xl md:text-2xl font-bold text-foreground">Pharma Mind Nexus</h1>
            <p className="mt-1 text-xs md:text-sm text-muted-foreground">
              AI-Powered Pharmaceutical Analytics
            </p>
          </div>

          <Card className="shadow-card hover:shadow-elevated transition-all duration-300 border-border/50 glass-effect transform hover:-translate-y-1">
            <CardHeader className="space-y-1 pb-4">
              <CardTitle className="text-xl md:text-2xl font-semibold">
                Reset Password
              </CardTitle>
              <CardDescription className="text-xs md:text-sm">
                Enter your email to receive password reset instructions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-3 md:space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="reset-email" className="text-xs md:text-sm">Email</Label>
                  <Input
                    id="reset-email"
                    type="email"
                    placeholder="sarah.chen@pharma.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
                  />
                </div>
                <Button 
                  type="submit" 
                  className="w-full text-sm md:text-base bg-gradient-medical hover:opacity-90 transition-all duration-300 hover:shadow-lg transform hover:scale-105 font-medium"
                  size="lg"
                >
                  Send Reset Link
                </Button>
              </form>

              <div className="mt-4 md:mt-6 text-center">
                <button
                  type="button"
                  onClick={() => setIsForgotPassword(false)}
                  className="text-xs md:text-sm text-muted-foreground hover:text-primary transition-colors inline-flex items-center gap-2 font-medium"
                >
                  <ArrowLeft className="h-3 w-3" />
                  Back to Login
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="mb-6 md:mb-8 text-center">
          <div className="mx-auto mb-3 md:mb-4 flex h-12 w-12 md:h-16 md:w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary/80 shadow-lg transform transition-transform hover:scale-110">
            <Database className="h-6 w-6 md:h-8 md:w-8 text-primary-foreground" />
          </div>
          <h1 className="text-xl md:text-2xl font-bold text-foreground">Pharma Mind Nexus</h1>
          <p className="mt-1 text-xs md:text-sm text-muted-foreground">
            AI-Powered Pharmaceutical Analytics
          </p>
        </div>

        <Card className="shadow-card hover:shadow-elevated transition-all duration-300 border-border/50 glass-effect transform hover:-translate-y-1">
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
                <>
                  <div className="space-y-2">
                    <Label htmlFor="name" className="text-xs md:text-sm">Full Name</Label>
                    <Input
                      id="name"
                      type="text"
                      placeholder="Dr. Sarah Chen"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                      className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="signup-role" className="text-xs md:text-sm">Role</Label>
                    <Input
                      id="signup-role"
                      type="text"
                      placeholder="Lead Researcher"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      required
                      className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
                    />
                  </div>
                </>
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
                  className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
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
                  className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
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
                    className="bg-input text-sm border-border focus:ring-2 focus:ring-primary/30 transition-all"
                  />
                </div>
              )}
              <Button 
                type="submit" 
                className="w-full text-sm md:text-base bg-gradient-medical hover:opacity-90 transition-all duration-300 hover:shadow-lg transform hover:scale-105 font-medium"
                size="lg"
              >
                {isSignup ? "Create Account" : "Sign In"}
              </Button>
            </form>

            <div className="mt-4 md:mt-6 text-center">
              <span className="text-xs md:text-sm text-muted-foreground">
                {isSignup ? "Already have an account? " : "Don't have an account? "}
              </span>
              <button
                type="button"
                onClick={handleToggleSignup}
                className="text-xs md:text-sm text-primary hover:text-primary/80 transition-colors font-medium transform hover:scale-105 ml-1"
              >
                {isSignup ? "Sign in" : "Sign up"}
              </button>
              {!isSignup && (
                <div className="mt-3">
                  <button
                    type="button"
                    onClick={() => setIsForgotPassword(true)}
                    className="text-xs md:text-sm text-primary hover:text-primary/80 transition-colors font-medium transform hover:scale-105"
                  >
                    Forgot password?
                  </button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}