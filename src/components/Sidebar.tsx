import { Home, MessageSquare, Users, FileText, Database, Settings, User } from "lucide-react";
import { NavLink } from "./NavLink";
import { cn } from "@/lib/utils";

const navigationItems = [
  { title: "Home", icon: Home, url: "/dashboard" },
  { title: "Chat", icon: MessageSquare, url: "/chat" },
  { title: "Worker Agents", icon: Users, url: "/agents" },
  { title: "Reports", icon: FileText, url: "/reports" },
  { title: "Knowledge Base", icon: Database, url: "/knowledge" },
  { title: "Settings", icon: Settings, url: "/settings" },
];

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-sidebar-border bg-sidebar">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex h-16 items-center border-b border-sidebar-border px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Database className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="text-lg font-semibold text-sidebar-foreground">
              Pharma AI Research
            </span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 overflow-y-auto p-4">
          {navigationItems.map((item) => (
            <NavLink
              key={item.url}
              to={item.url}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              )}
              activeClassName="bg-sidebar-accent text-sidebar-primary"
            >
              <item.icon className="h-5 w-5" />
              <span>{item.title}</span>
            </NavLink>
          ))}
        </nav>

        {/* Profile */}
        <div className="border-t border-sidebar-border p-4">
          <div className="flex items-center gap-3 rounded-lg bg-sidebar-accent px-3 py-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground">
              <User className="h-5 w-5" />
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="truncate text-sm font-medium text-sidebar-foreground">
                Dr. Sarah Chen
              </p>
              <p className="truncate text-xs text-muted-foreground">
                Lead Researcher
              </p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
