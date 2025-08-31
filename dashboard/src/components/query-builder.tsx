import { QueryBuilderShadcn as BaseQueryBuilderShadcn } from "react-querybuilder-shadcn";
import * as BaseQueryBuilder from "react-querybuilder";

import "react-querybuilder-shadcn/dist/style.css";
import dynamic from "next/dynamic";

export type Fields = BaseQueryBuilder.OptionList<BaseQueryBuilder.Field> | Record<string, BaseQueryBuilder.Field>;
export type Query = BaseQueryBuilder.RuleGroupType;

interface QueryBuilderProps {
    fields?: Fields;
    query?: Query;
    onQueryChange?: (query: Query) => void;
}

function QB({ fields, query, onQueryChange }: QueryBuilderProps) {
    return (
        <BaseQueryBuilderShadcn>
            <BaseQueryBuilder.QueryBuilder
                fields={fields}
                query={query}
                onQueryChange={onQueryChange}
            />
        </BaseQueryBuilderShadcn>
    );
}

// Lazy-load without SSR
export const QueryBuilder = dynamic(() => Promise.resolve(QB), {
  ssr: false,
});