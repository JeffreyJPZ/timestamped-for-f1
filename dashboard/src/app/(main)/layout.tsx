import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

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