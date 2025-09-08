// Credit to Bulletproof React https://github.com/alan2207/bulletproof-react/blob/49c4249fd68ef2196151ef34cc2c68cb4fe81dc1/apps/nextjs-app/src/lib/react-query.ts

import { QueryClient, QueryClientConfig, UseMutationOptions } from "@tanstack/react-query";

const queryClientConfig: QueryClientConfig = {
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: true,
            staleTime: 10 * 60 * 1000 // Cache data for 10 minutes
        },
    },
}

export const queryClient = new QueryClient(queryClientConfig);


// TODO: fix "any" typing
export type ApiFnReturnType<FnType extends (...params: any) => Promise<any>> =
  Awaited<ReturnType<FnType>>;

export type QueryConfig<T extends (...args: any) => any> = Omit<
  ReturnType<T>,
  'queryKey' | 'queryFn'
>;

export type MutationConfig<
  MutationFnType extends (...args: any) => Promise<any>,
> = UseMutationOptions<
  ApiFnReturnType<MutationFnType>,
  Error,
  Parameters<MutationFnType>[0]
>;