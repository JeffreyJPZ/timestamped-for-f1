import { queryOptions, useQuery } from '@tanstack/react-query';
import { Event, EventsRead } from '@/types/event';
import { QueryConfig } from '@/lib/react-query';

async function getEvents({ category, cause, date, meeting_key, session_key }: EventsRead): Promise<Event[]> {
    return [];
}

export function getEventsQueryOptions({ category, cause, date, meeting_key, session_key }: EventsRead) {
    return queryOptions({
        queryKey: ["events", meeting_key, session_key, { category, cause, date }],
        queryFn: () => getEvents({ category, cause, date, meeting_key, session_key })
    });
}

type UseGetEventsOptions = EventsRead & {
    queryConfig?: QueryConfig<typeof getEventsQueryOptions>;
}

export function useGetEvents({ queryConfig, category, cause, date, meeting_key, session_key }: UseGetEventsOptions) {
    return useQuery({
        ...getEventsQueryOptions({ category, cause, date, meeting_key, session_key }),
        ...queryConfig
    });
}