"use client"

import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/react-query";
import { Home } from "@/app/home";

export default function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <Home />
        </QueryClientProvider>
    );
}
