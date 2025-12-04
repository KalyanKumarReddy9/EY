import { Menu } from "lucide-react";
import { Button } from "./ui/button";

interface MobileHeaderProps {
  onMenuClick: () => void;
}

export function MobileHeader({ onMenuClick }: MobileHeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex h-14 items-center border-b border-border bg-background/95 backdrop-blur-sm px-4 md:hidden">
      <Button
        variant="ghost"
        size="icon"
        onClick={onMenuClick}
        className="mr-3"
      >
        <Menu className="h-5 w-5" />
      </Button>
      <div className="flex items-center gap-2">
        <span className="text-base font-semibold text-foreground">
          Pharma Mind Nexus
        </span>
      </div>
    </header>
  );
}
