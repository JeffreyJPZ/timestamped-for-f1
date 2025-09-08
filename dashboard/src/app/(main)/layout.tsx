import { type Metadata } from "next";

import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export const metadata: Metadata = {
  title: "Home | Timestamped for F1",
  description: "A play-by-play/events archive for Formula 1.",
};

export default function HomeLayout({ children }: {
    children: React.ReactNode;
}) {
    return (
        <SidebarProvider>
            <AppSidebar />
            <div className="w-full overflow-hidden">
                {children}
            </div>
        </SidebarProvider>
    );
}