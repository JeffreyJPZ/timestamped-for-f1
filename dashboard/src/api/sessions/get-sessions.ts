import { queryOptions, useQuery } from "@tanstack/react-query";
import { type QueryConfig } from "@/lib/react-query";
import { getQueryURL } from "@/lib/web-api";
import { sessions, type Sessions, type SessionsRead } from "@/types/session";

async function getSessions(params: SessionsRead): Promise<Sessions> {
    const url = getQueryURL("sessions", params);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/sessions request failure`);
    }
    
    const data = await response.json();
    const sessionsParseResult = sessions.safeParse(data);
    
    if (!sessionsParseResult.success) {
        console.error(sessionsParseResult.error);
        throw sessionsParseResult.error;
    }

    return sessionsParseResult.data;
}

export function getSessionsQueryOptions(params: SessionsRead) {
    return queryOptions({
        queryKey: ["sessions", { ...params }],
        queryFn: () => getSessions(params)
    });
}

type UseGetSessionsOptions = SessionsRead & {
    queryConfig?: QueryConfig<typeof getSessionsQueryOptions>;
}

export function useGetSessions({ queryConfig, ...params }: UseGetSessionsOptions) {
    return useQuery({
        ...getSessionsQueryOptions(params),
        ...queryConfig
    });
}