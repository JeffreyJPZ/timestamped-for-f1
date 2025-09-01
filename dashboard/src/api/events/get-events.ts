import { queryOptions, useQuery } from "@tanstack/react-query";
import { type Events, events, type EventsRead } from "@/types/event";
import { type QueryConfig } from "@/lib/react-query";
import { getQueryURL } from "@/lib/web-api";

async function getEvents(params: EventsRead): Promise<Events> {
    const url = getQueryURL("events", params);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/events request failure`);
    }
    
    const data = await response.json();
    const eventsParseResult = events.safeParse(data);
    
    if (!eventsParseResult.success) {
        console.error(eventsParseResult.error);
        throw eventsParseResult.error;
    }

    return eventsParseResult.data;
}

export function getEventsQueryOptions(params: EventsRead) {
    return queryOptions({
        queryKey: ["events", { ...params }],
        queryFn: () => getEvents(params)
    });
}

type UseGetEventsOptions = EventsRead & {
    queryConfig?: QueryConfig<typeof getEventsQueryOptions>;
}

export function useGetEvents({ queryConfig, ...params }: UseGetEventsOptions) {
    return useQuery({
        ...getEventsQueryOptions(params),
        ...queryConfig
    });
}