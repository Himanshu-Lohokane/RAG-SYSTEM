"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  Upload, 
  Search, 
  FileText, 
  Shield, 
  Settings,
  Users,
  BarChart3
} from "lucide-react";

const navigationItems = [
  {
    title: "AI Assistant",
    href: "/search",
    icon: Search,
  },
  {
    title: "Upload Documents",
    href: "/upload",
    icon: Upload,
  },
];

export const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-gradient-to-b from-card to-background h-[calc(100vh-4rem)] shadow-md">
      <nav className="p-6 space-y-4">
        {navigationItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group flex items-center gap-4 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 relative overflow-hidden",
                "hover:scale-105 transform",
                isActive
                  ? "bg-primary text-primary-foreground shadow-lg"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
              )}
            >
              <div className={cn(
                "absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity",
                "bg-gradient-to-r from-primary to-primary/50"
              )} />
              <item.icon className={cn(
                "h-5 w-5 transition-transform duration-200",
                "group-hover:rotate-6 group-hover:scale-110"
              )} />
              <span className="relative z-10 tracking-wide">
                {item.title}
              </span>
              {isActive && (
                <div className="absolute right-2 w-1.5 h-1.5 rounded-full bg-primary-foreground/80" />
              )}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};