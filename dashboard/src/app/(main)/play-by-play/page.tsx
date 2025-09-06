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
import { Skeleton } from "@/components/ui/skeleton";
import { Events } from "@/types/event";
import { useCallback, useState } from "react";

export default function PlayByPlay() {
  const [selectedSeason, setSelectedSeason] = useState<number>(0);
  const [selectedMeetingKey, setSelectedMeetingKey] = useState<number>(0);
  const [selectedSessionKey, setSelectedSessionKey] = useState<number>(0);

  const seasonsQuery = useGetSeasons({});
  const meetingsQuery = useGetMeetings({
    queryConfig: { enabled: !!selectedSeason },
    year: [selectedSeason]
  });
  const sessionsQuery = useGetSessions({
    queryConfig: { enabled: !!selectedMeetingKey },
    meeting_key: [selectedMeetingKey]
  });

  // Returns events in chronological order
  const sortEventsByDate = useCallback((events: Events) => {
    return events.sort((a, b) => {
      return new Date(a.date).getTime() - new Date(b.date).getTime()
    });
  }, []);

  const eventsQuery = useGetEvents({
    queryConfig: {
      enabled: !!(selectedSeason && selectedMeetingKey && selectedSessionKey),
      select: sortEventsByDate
    },
    session_key: [selectedSessionKey]
  });
  
  return (
    <div className="flex flex-col items-center justify-items-center w-full">
      <header className="flex max-h-xl shrink-0 items-center gap-2 border-b p-4 w-full">
        <div className="flex gap-4 items-center w-full">
          <div className="-ml-1">
            <SidebarTrigger />
          </div>
          <div className="flex flex-wrap gap-4">
            <Select onValueChange={(value) => {
              // "Clear" the dependent select values
              const season = parseInt(value);
              if (season !== selectedSeason) {
                setSelectedMeetingKey(0);
                setSelectedSessionKey(0);
              }

              setSelectedSeason(season);
            }}>
              <SelectTrigger className="w-32">
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
            <Select onValueChange={(value) => {
              // "Clear" the dependent select values
              const meetingKey = parseInt(value);
              if (meetingKey !== selectedMeetingKey) {
                setSelectedSessionKey(0);
              }

              setSelectedMeetingKey(meetingKey);
            }}>
              <SelectTrigger className="w-64">
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
              <SelectTrigger className="w-64">
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
        {eventsQuery.isFetching
          ? <>
              <Skeleton className="h-60 w-xl rounded-xl" />
              <Skeleton className="h-60 w-xl rounded-xl" />
              <Skeleton className="h-60 w-xl rounded-xl" />
              <Skeleton className="h-60 w-xl rounded-xl" />
              <Skeleton className="h-60 w-xl rounded-xl" />
            </>
          : eventsQuery.data?.map((event) => <EventCard key={JSON.stringify(event)} event={event} />)
        }
      </main>
    </div>
  )
}
