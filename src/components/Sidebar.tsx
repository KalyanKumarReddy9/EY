import { Home, MessageSquare, Users, FileText, Database, Settings, User, X, LogOut, Search } from "lucide-react";
import { NavLink } from "./NavLink";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import { useEffect, useState } from "react";

const navigationItems = [
  { title: "Home", icon: Home, url: "/dashboard" },
  { title: "Chat", icon: MessageSquare, url: "/chat" },
  { title: "Worker Agents", icon: Users, url: "/agents" },
  { title: "Reports", icon: FileText, url: "/reports" },
  { title: "Knowledge Base", icon: Database, url: "/knowledge" },
  { title: "Settings", icon: Settings, url: "/settings" },
  
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [name, setName] = useState('');
  const [role, setRole] = useState('');

  useEffect(() => {
    try {
      const raw = localStorage.getItem('user');
      if (raw) {
        const u = JSON.parse(raw);
        setName(u?.name || '');
        setRole(u?.role || '');
      }
    } catch (e) {
      setName('');
      setRole('');
    }
  }, []);

  const handleLogout = () => {
    toast({
      title: "Logged Out",
      description: "You have been successfully logged out",
    });
    // clear local auth state
    try { localStorage.removeItem('token'); localStorage.removeItem('user'); } catch (e) {}
    navigate("/");
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-50 h-screen w-64 border-r border-sidebar-border bg-sidebar transition-transform duration-300",
          "md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex h-full flex-col">
          {/* Logo & Close Button */}
          <div className="flex h-14 md:h-16 items-center justify-between border-b border-sidebar-border px-4 md:px-6">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 md:h-8 md:w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-primary/80 shadow-sm">
                <Database className="h-3.5 w-3.5 md:h-4 md:w-4 text-primary-foreground" />
              </div>
              <span className="text-base md:text-lg font-semibold text-sidebar-foreground">
                Pharma Nexus
              </span>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={onClose}
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 overflow-y-auto p-3 md:p-4">
            {navigationItems.map((item) => (
              <NavLink
                key={item.url}
                to={item.url}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                  "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:translate-x-1"
                )}
                activeClassName="bg-sidebar-accent text-sidebar-primary"
                onClick={onClose}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                <span>{item.title}</span>
              </NavLink>
            ))}
          </nav>

          {/* Profile */}
          <div className="border-t border-sidebar-border p-3 md:p-4 space-y-3">
                <div className="flex items-center gap-3 rounded-lg bg-sidebar-accent px-3 py-2">
              <div className="flex h-8 w-8 md:h-9 md:w-9 items-center justify-center rounded-full bg-primary text-primary-foreground flex-shrink-0">
                <User className="h-4 w-4 md:h-5 md:w-5" />
              </div>
              <div className="flex-1 overflow-hidden">
                <p className="truncate text-sm font-medium text-sidebar-foreground">
                  {name || 'Guest User'}
                </p>
                <p className="truncate text-xs text-muted-foreground">
                  {role || 'Member'}
                </p>
              </div>
            </div>
            <Button 
              onClick={handleLogout}
              variant="outline" 
              className="w-full justify-start gap-2 text-sm border-destructive/30 text-destructive hover:bg-destructive/10 hover:text-destructive hover:border-destructive transition-colors"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </aside>
    </>
  );
}
