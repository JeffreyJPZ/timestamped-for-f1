"use client";

import { useGetEvents } from "@/api/events/get-events";
import { EventCard } from "@/components/event-card";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { SidebarTrigger } from "@/components/ui/sidebar";

export default function Dashboard() {
  const events = useGetEvents({});
  
  return (
    <div className="w-full">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <div className="flex">
          <SidebarTrigger className="-ml-1" />
          <Select>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Season" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="2024">2024</SelectItem>
            </SelectContent>
          </Select>
          <Select>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Meeting" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="São Paulo Grand Prix">São Paulo Grand Prix</SelectItem>
            </SelectContent>
          </Select>
          <Select>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Session" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Practice 1">Practice 1</SelectItem>
              <SelectItem value="Sprint Qualifying">Sprint Qualifying</SelectItem>
              <SelectItem value="Sprint">Sprint</SelectItem>
              <SelectItem value="Qualifying">Qualifying</SelectItem>
              <SelectItem value="Race">Race</SelectItem>
            </SelectContent>
          </Select>
          <Button>Get Events</Button>
        </div>
      </header>
      {events.isSuccess && events.data.map((event) => <EventCard event={event} />)}
      <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          <div className="bg-muted/50 aspect-video rounded-xl" />
          <div className="bg-muted/50 aspect-video rounded-xl" />
          <div className="bg-muted/50 aspect-video rounded-xl" />
        </div>
        <div className="bg-muted/50 min-h-[100vh] flex-1 rounded-xl md:min-h-min" />
      </div>
    </div>
  )
}
