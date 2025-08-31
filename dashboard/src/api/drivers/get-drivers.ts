import { queryOptions, useQuery } from '@tanstack/react-query';
import { Drivers, drivers, DriversRead } from '@/types/driver';
import { QueryConfig } from '@/lib/react-query';
import { getQueryURL } from '@/lib/web-api';

async function getDrivers(params: DriversRead): Promise<Drivers> {
    const url = getQueryURL("drivers", params);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`/drivers request failure`);
    }
    
    const data = await response.json();
    const parseResult = drivers.safeParse(data);
    
    if (!parseResult.success) {
        console.error(parseResult.error);
        throw parseResult.error;
    }

    return parseResult.data;
}

export function getDriversQueryOptions(params: DriversRead) {
    return queryOptions({
        queryKey: ["drivers", { ...params }],
        queryFn: () => getDrivers(params)
    });
}

type UseGetDriversOptions = DriversRead & {
    queryConfig?: QueryConfig<typeof getDriversQueryOptions>;
}

export function useGetDrivers({ queryConfig, ...params }: UseGetDriversOptions) {
    return useQuery({
        ...getDriversQueryOptions(params),
        ...queryConfig
    });
}