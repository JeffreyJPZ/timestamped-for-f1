import { queryOptions, useQuery } from "@tanstack/react-query";
import { meetings } from "@/types/meeting";
import { season, seasons, type Seasons } from "@/types/season";
import { type QueryConfig } from "@/lib/react-query";
import { getQueryURL } from "@/lib/web-api";

async function getSeasons(): Promise<Seasons> {
    // Derive seasons from meeetings
    const url = getQueryURL("meetings");
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

    // Transform to seasons
    const uniqueSeasons = new Set<number>();
    meetingsParseResult.data.forEach((meeting) => uniqueSeasons.add(meeting.year));

    const seasons: Seasons = [];
    uniqueSeasons.entries().forEach(([season, _]) => {
        seasons.push({year: season});
    });

    return seasons;
}

export function getSeasonsQueryOptions() {
    return queryOptions({
        queryKey: ["seasons"],
        queryFn: () => getSeasons()
    });
}

type UseGetSeasonsOptions = {
    queryConfig?: QueryConfig<typeof getSeasonsQueryOptions>;
}

export function useGetSeasons({ queryConfig }: UseGetSeasonsOptions) {
    return useQuery({
        ...getSeasonsQueryOptions(),
        ...queryConfig
    });
}