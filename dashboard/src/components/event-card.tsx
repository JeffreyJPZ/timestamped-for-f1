import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Event } from "@/types/event";
import { Badge } from "./ui/badge";
import { useGetDrivers } from "@/api/drivers/get-drivers";
import { useGetSession } from "@/api/sessions/get-session";

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
    second: "2-digit",
    timeZone: "UTC"
  });

  return formatter.format(new Date(date));
}

// Returns only the whole part of a time string.
function trimFractionalSeconds(time: string): string {
    return time.split(".")[0];
}

// Formats a lap time in seconds as M:SS.SSS.
function formatLapDuration(time: number): string {
  const date = new Date(0);
  date.setMilliseconds(time * 1000);

  return date.toISOString().substring(15, 23);
}

export function EventCard({ event }: EventCardProps) {
  const drivers = useGetDrivers({
    session_key: [event.session_key]
  });
  const session = useGetSession({
    session_key: event.session_key
  });

  // if incident/incident verdict, use message, otherwise format message as {initiator} {event cause}
  function formatDriverEventMessage(event: Event): string {
    // Maximum of one initiator
    const initiatorDriverRole = event.details?.driver_roles
    ? Object.entries(event.details?.driver_roles)
      .find((driver) => {
        return driver[1] === "initiator"; // Get driver role
      })
    : null;

    const initiatorDriver = initiatorDriverRole
      ? drivers.data?.find((driver) => `${driver.driver_number}` == initiatorDriverRole[0])
      : null;
    
    // Multiple participants allowed
    const participantDriverRoles = event.details?.driver_roles
    ? Object.entries(event.details?.driver_roles)
      .filter((driver) => {
        return driver[1] === "participant";
      })
    : null;
    
    const participantDriverNumbers = participantDriverRoles
      ? participantDriverRoles.map((driver) => driver[0]) // Get driver number
      : null;
    
    const participantDrivers = participantDriverNumbers
      ? drivers.data?.filter((driver) => participantDriverNumbers.includes(`${driver.driver_number}`))
      : null;

    if (!initiatorDriver) {
      return "";
    }

    switch (event.cause) {
      case "black-flag":
      case "black-and-orange-flag":
      case "black-and-white-flag":
      case "blue-flag":
      case "incident":
      case "incident-verdict":
      case "track-limits":
        return `${event.details?.message}`;
      case "out":
        return `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) OUT OF THE SESSION`;
      case "overtake":
        return participantDrivers
          ? `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) OVERTAKES CAR ${participantDrivers[0].driver_number} (${participantDrivers[0].name_acronym}) FOR P${event.details?.position}`
          : "";
      case "personal-best-lap":
        return event.details?.position
          ? `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) ${event.details?.lap_duration ? formatLapDuration(event.details?.lap_duration) : ""} PERSONAL BEST TIME FOR P${event.details?.position}`
          : `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) ${event.details?.lap_duration ? formatLapDuration(event.details?.lap_duration) : ""} PERSONAL BEST TIME`;
      case "pit":
        return event.details?.pit_stop_duration
          ? `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) ${event.details?.pit_stop_duration} SECONDS PIT STOP FOR ${(event.details?.tyre_age_at_start !== null && event.details?.tyre_age_at_start !== undefined) ? event.details?.tyre_age_at_start > 0 ? "USED " : "NEW " : " "}${event.details?.compound} TYRES`
          : `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) PIT STOP FOR ${event.details?.compound} TYRES`;
      case "provisional-classification":
        return `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) FINISHES THE SESSION IN P${event.details?.position}`;
      case "qualifying-stage-classification":
        return event.details?.eliminated
          ? `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) ELIMINATED FROM Q${event.details?.qualifying_stage_number} IN P${event.details?.position}`
          : `CAR ${initiatorDriver.driver_number} (${initiatorDriver.name_acronym}) ADVANCES FROM Q${event.details?.qualifying_stage_number} IN P${event.details?.position}`;
      default:
        return "";
    }


  }

  function toMessage(event: Event): string {
    switch (event.category) {
      case "driver-action":
      case "driver-notification":
        return formatDriverEventMessage(event);
      case "sector-notification":
      case "track-notification":
      case "other":
        return `${event.details?.message}`;
      default:
        return "";
    }
  }

  return (
    <Card className="max-w-xl w-full">
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
        {/* Skip displaying lap number for non-race sessions since they are associated with drivers */}
        {(session.data?.session_type === "Race" && event.details?.lap_number) &&
          <CardDescription>
            Lap {event.details.lap_number}
          </CardDescription>
        }
      </CardHeader>
      <CardContent>
        <CardDescription>
          {toMessage(event)}
        </CardDescription>
      </CardContent>
      <CardFooter className="flex flex-wrap gap-2">
        {event.details
          ? Object.entries(event.details)
              .filter((details) => {
                return details[1] !== null; // Filter out null values
              })
              .map(([key, value]) => {
                return (
                  <Badge className="whitespace-normal" key={`${key}-${JSON.stringify(value)}`} variant="secondary">
                    {key}: {JSON.stringify(value)}
                  </Badge>
                );
          })
          : null
        }
      </CardFooter>
    </Card>
  )
}