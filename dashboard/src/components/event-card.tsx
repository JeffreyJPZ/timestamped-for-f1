import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Event } from "@/types/event";
import { Badge } from "./ui/badge";

interface EventCardProps {
  event: Event;
}

function toTitle(input: string): string {
  return input
    .toLocaleLowerCase()
    .replace(/-/g, ' ')                   // Replace hyphens with spaces
    .replace(/\b\w/g, char => char.toUpperCase()); // Capitalize first letter of each word
}

function toLocaleDate(date: string): string {
  // Use browser default locale
  const formatter = new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });

  return formatter.format(new Date(date));
}

// Returns only the whole part of a time string.
function trimFractionalSeconds(time: string): string {
    return time.split(".")[0];
}

function toMessage(event: Event): string {
  switch (event.category) {
    case "driver-action":
    case "driver-notification":
      return "";
    case "session-notification":
      return "";
    case "sector-notification":
    case "track-notification":
    case "other":
      return `${event.details?.message}`;
  }
}

export function EventCard({ event }: EventCardProps) {

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>
          {toTitle(event.cause)}
        </CardTitle>
        <CardDescription>
          {toLocaleDate(event.date)}
        </CardDescription>
        <CardDescription>
          {trimFractionalSeconds(event.elapsed_time)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <CardDescription>
          {toMessage(event)}
        </CardDescription>
      </CardContent>
      <CardFooter className="flex gap-2">
        {event.details
          ? Object.entries(event.details).map(([key, value]) => {
            return <Badge key={key + JSON.stringify(value)}>{key}: {JSON.stringify(value)}</Badge>
          })
          : null
        }
      </CardFooter>
    </Card>
  )
}