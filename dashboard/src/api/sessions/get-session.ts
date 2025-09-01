import { queryOptions, skipToken, useQuery } from "@tanstack/react-query";
import { type Session, session, type SessionRead } from "@/types/session";
import { type QueryConfig } from "@/lib/react-query";
import { getQueryURL } from "@/lib/web-api";

async function getSession(params: SessionRead): Promise<Session> {
    const url = getQueryURL(`/sessions/${params.session_key}`);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/sessions/${params.session_key} request failure`);
    }
    
    const data = await response.json();
    const sessionParseResult = session.safeParse(data);
    
    if (!sessionParseResult.success) {
        console.error(sessionParseResult.error);
        throw sessionParseResult.error;
    }

    return sessionParseResult.data;
}

export function getSessionQueryOptions(params: SessionRead) {
    return queryOptions({
        queryKey: ["session", params.session_key],
        queryFn: params.session_key ? () => getSession(params) : skipToken
    });
}

type UseGetSessionOptions = SessionRead & {
    queryConfig?: QueryConfig<typeof getSessionQueryOptions>;
}

export function useGetSession({ queryConfig, ...params }: UseGetSessionOptions) {
    return useQuery({
        ...getSessionQueryOptions(params),
        ...queryConfig
    });
}