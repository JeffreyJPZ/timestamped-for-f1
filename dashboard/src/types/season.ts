import z from "zod";

export const season = z.object({
    year: z.number().int().positive()
});

export const seasons = z.array(season);

export type Season = z.infer<typeof season>;
export type Seasons = z.infer<typeof seasons>;