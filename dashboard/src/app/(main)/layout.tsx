import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export default function HomeLayout({ children }: {
    children: React.ReactNode;
}) {
    return (
        <SidebarProvider>
            <AppSidebar collapsible="icon"/>
            <main>
                {children}
            </main>
        </SidebarProvider>
    );
}