import { QueryBuilderShadcn as ReactQueryBuilderShadcn} from "react-querybuilder-shadcn";
import { Field, OptionList, QueryBuilder as ReactQueryBuilder, RuleGroupType } from "react-querybuilder";

import "react-querybuilder-shadcn/dist/style.css";

export type Fields = OptionList<Field> | Record<string, Field>;
export type Query = RuleGroupType;

interface QueryBuilderProps {
    fields?: Fields;
    query?: Query;
    onQueryChange?: (query: Query) => void;
}

export function QueryBuilder({ fields, query, onQueryChange }: QueryBuilderProps) {
    return (
        <ReactQueryBuilderShadcn>
            <ReactQueryBuilder
                fields={fields}
                query={query}
                onQueryChange={onQueryChange}
            />
        </ReactQueryBuilderShadcn>
    );
}