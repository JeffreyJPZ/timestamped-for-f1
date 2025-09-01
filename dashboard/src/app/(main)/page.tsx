"use client";

import Image from "next/image";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { SquareChartGantt } from "lucide-react";
import Link from "next/link";

export default function Home() {
    return (
        <div className="w-full">
            <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4 w-full">
                <SidebarTrigger className="-ml-1" />
            </header>
            <div className="flex flex-col items-center justify-center min-h-screen px-8 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
                <main className="flex flex-col gap-4 items-center sm:items-start">
                    <h1 className="font-bold self-center text-5xl text-center">Timestamped for F1</h1>
                    <h2 className="max-w-xl self-center text-center">A play-by-play/events archive for Formula 1. View overtakes, qualifying laps, pit stops, incidents, and more as they happened. </h2>
                    <div className="flex gap-4 items-center flex-col sm:flex-row self-center">
                        <Link
                        className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
                        href="/play-by-play"
                        >
                            <SquareChartGantt />
                            <p className="text-md">
                                Play-by-Play
                            </p>
                        </Link>
                    </div>
                </main>
            </div>
            <footer className="flex gap-4 flex-wrap items-center justify-center p-8">
                <a
                className="flex items-center gap-4 hover:underline hover:underline-offset-4"
                href="https://github.com/JeffreyJPZ/timestamped-for-f1"
                target="_blank"
                rel="noopener noreferrer"
                >
                    <Image
                    className=""
                    aria-hidden
                    src="/icons/links/github-mark.svg"
                    alt="GitHub logo"
                    width={16}
                    height={16}
                    />
                    <p className="text-sm">
                        JeffreyJPZ/timestamped-for-f1
                    </p>
                </a>
                <p className="text-sm">
                    Version 0.1.0
                </p>
                <p className="text-sm">
                    Timestamped for F1 is unofficial and is not associated in any way with the Formula 1 companies.
                    F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX
                    and related marks are trade marks of Formula One Licensing B.V.
                </p>
            </footer>
        </div>
    );
}