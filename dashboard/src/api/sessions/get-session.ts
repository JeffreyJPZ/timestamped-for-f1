import { queryOptions, skipToken, useQuery } from '@tanstack/react-query';
import { Session, session, SessionRead } from '@/types/session';
import { QueryConfig } from '@/lib/react-query';
import { getQueryURL } from '@/lib/web-api';

async function getSession(params: SessionRead): Promise<Session> {
    const url = getQueryURL(`/sessions/${params.session_key}`);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/sessions/${params.session_key} request failure`);
    }
    
    const data = await response.json();
    const parseResult = session.safeParse(data);
    
    if (!parseResult.success) {
        console.error(parseResult.error);
        throw parseResult.error;
    }

    return parseResult.data;
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