import { QueryClient, QueryClientConfig, UseMutationOptions } from "@tanstack/react-query";

const queryClientConfig: QueryClientConfig = {
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: true,
            staleTime: 0
        },
    },
}

export const queryClient = new QueryClient(queryClientConfig);

export type ApiFnReturnType<FnType extends (...args: any) => Promise<any>> =
  Awaited<ReturnType<FnType>>;

export type QueryConfig<T extends (...args: any[]) => any> = Omit<
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