import { type Metadata } from "next";

export const metadata: Metadata = {
  title: "Play-by-Play | Timestamped for F1",
  description: "View all events in a session chronologically.",
};

export default function PlayByPlayLayout({ children }: {
    children: React.ReactNode;
}) {
    return (
        <div className="w-full">
            {children}
        </div>
    );
}