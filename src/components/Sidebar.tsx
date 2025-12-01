import { Home, MessageSquare, Users, FileText, Database, Settings, User, X } from "lucide-react";
import { NavLink } from "./NavLink";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

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
              <div className="flex h-7 w-7 md:h-8 md:w-8 items-center justify-center rounded-lg bg-primary">
                <Database className="h-3.5 w-3.5 md:h-4 md:w-4 text-primary-foreground" />
              </div>
              <span className="text-base md:text-lg font-semibold text-sidebar-foreground">
                Pharma AI
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
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                  "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
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
          <div className="border-t border-sidebar-border p-3 md:p-4">
            <div className="flex items-center gap-3 rounded-lg bg-sidebar-accent px-3 py-2">
              <div className="flex h-8 w-8 md:h-9 md:w-9 items-center justify-center rounded-full bg-primary text-primary-foreground flex-shrink-0">
                <User className="h-4 w-4 md:h-5 md:w-5" />
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
    </>
  );
}
