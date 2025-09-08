import { type Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { RootProviders } from "./root-providers";

import "@/styles/globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Timestamped for F1",
  description: "A play-by-play/events archive for Formula 1.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <RootProviders>
          {children}
        </RootProviders>
      </body>
    </html>
  );
}
