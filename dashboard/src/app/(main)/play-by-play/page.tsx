"use client";

import { useGetEvents } from "@/api/events/get-events";
import { useGetMeetings } from "@/api/meetings/get-meetings";
import { useGetSeasons } from "@/api/seasons/get-seasons";
import { useGetSessions } from "@/api/sessions/get-sessions";
import { EventCard } from "@/components/event-card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useState } from "react";

export default function PlayByPlay() {
  const [selectedSeason, setSelectedSeason] = useState<number>();
  const [selectedMeetingKey, setSelectedMeetingKey] = useState<number>();
  const [selectedSessionKey, setSelectedSessionKey] = useState<number>();

  const seasonsQuery = useGetSeasons({});
  const meetingsQuery = useGetMeetings(
    selectedSeason
    ? { year: [selectedSeason] }
    : { year: [0] } // Should return empty list 
  );
  const sessionsQuery = useGetSessions(
    selectedSeason && selectedMeetingKey
    ? { meeting_key: [selectedMeetingKey] }
    : { meeting_key: [0] }
  );
  const eventsQuery = useGetEvents(
    selectedSeason && selectedMeetingKey && selectedSessionKey
    ? { session_key: [selectedSessionKey] }
    : { session_key: [0] }
  );

  return (
    <div className="flex flex-col items-center justify-items-center w-full">
      <header className="flex max-h-xl shrink-0 items-center gap-2 border-b p-4 w-full">
        <div className="flex gap-4 items-center w-full">
          <div className="-ml-1">
            <SidebarTrigger />
          </div>
          <div className="flex flex-wrap gap-4">
            <Select onValueChange={(value) => setSelectedSeason(parseInt(value))}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Season" />
              </SelectTrigger>
              {(seasonsQuery.isSuccess && seasonsQuery.data?.length > 0) &&
                <SelectContent>
                  {seasonsQuery.data.map(
                    (season) => {
                      return (
                        <SelectItem
                        key={JSON.stringify(season.year)}
                        value={JSON.stringify(season.year)}
                        >
                          {season.year}
                        </SelectItem>
                      );
                    })
                  }
                </SelectContent>
              }
            </Select>
            <Select onValueChange={(value) => setSelectedMeetingKey(parseInt(value))}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Meeting" />
              </SelectTrigger>
              {(meetingsQuery.isSuccess && meetingsQuery.data?.length > 0) &&
                <SelectContent>
                  {meetingsQuery.data.map(
                    (meeting) => {
                      return (
                        <SelectItem
                        key={JSON.stringify(meeting.meeting_key)}
                        value={JSON.stringify(meeting.meeting_key)}
                        >
                          {meeting.meeting_name}
                        </SelectItem>
                      );
                    })
                  }
                </SelectContent>
              }
            </Select>
            <Select onValueChange={(value) => setSelectedSessionKey(parseInt(value))}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Session" />
              </SelectTrigger>
              {(sessionsQuery.isSuccess && sessionsQuery.data?.length > 0) &&
                <SelectContent>
                  {sessionsQuery.data?.map(
                    (session) => {
                      return (
                        <SelectItem
                        key={JSON.stringify(session.session_key)}
                        value={JSON.stringify(session.session_key)}
                        >
                          {session.session_name}
                        </SelectItem>
                      );
                    })
                  }
                </SelectContent>
              }
            </Select>
          </div>
        </div>
      </header>
      <main className="flex flex-col gap-8 p-8 items-center w-full">
        {eventsQuery.data?.map((event) => <EventCard key={JSON.stringify(event)} event={event} />)}
      </main>
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
