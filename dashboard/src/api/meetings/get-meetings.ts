import { queryOptions, useQuery } from "@tanstack/react-query";
import { type Meetings, meetings, type MeetingsRead } from "@/types/meeting";
import { type QueryConfig } from "@/lib/react-query";
import { getQueryURL } from "@/lib/web-api";

async function getMeetings(params: MeetingsRead): Promise<Meetings> {
    const url = getQueryURL("meetings", params);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/meetings request failure`);
    }
    
    const data = await response.json();
    const meetingsParseResult = meetings.safeParse(data);
    
    if (!meetingsParseResult.success) {
        console.error(meetingsParseResult.error);
        throw meetingsParseResult.error;
    }

    return meetingsParseResult.data;
}

export function getMeetingsQueryOptions(params: MeetingsRead) {
    return queryOptions({
        queryKey: ["meetings", { ...params }],
        queryFn: () => getMeetings(params)
    });
}

type UseGetMeetingsOptions = MeetingsRead & {
    queryConfig?: QueryConfig<typeof getMeetingsQueryOptions>;
}

export function useGetMeetings({ queryConfig, ...params }: UseGetMeetingsOptions) {
    return useQuery({
        ...getMeetingsQueryOptions(params),
        ...queryConfig
    });
}