import { queryOptions, useQuery } from '@tanstack/react-query';
import { Events, events, EventsRead } from '@/types/event';
import { QueryConfig } from '@/lib/react-query';
import { Endpoint, getQueryURL } from '@/lib/web-api';

async function getEvents(params: EventsRead): Promise<Events> {
    const endpoint: Endpoint = "events";
    const url = getQueryURL(endpoint, params);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`${endpoint} request failure`);
    }
    
    const data = await response.json();
    const parseResult = events.safeParse(data);
    
    if (!parseResult.success) {
        console.error(parseResult.error);
        throw parseResult.error;
    }

    return parseResult.data;
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