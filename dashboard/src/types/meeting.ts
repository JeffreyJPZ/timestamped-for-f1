import z from "zod";

const meetingSchema = z
    .object({
        circuit_key: z.number().int().positive(),
        circuit_short_name: z.string(),
        country_code: z.string().length(3),
        country_key: z.number().int().positive(),
        country_name: z.string(),
        date_start: z.iso.datetime(),
        gmt_offset: z.string().regex(/^[-+]\d{2}:\d{2}:\d{2}$/),
        location: z.string(),
        meeting_key: z.number().int().positive(),
        meeting_name: z.string(),
        meeting_official_name: z.string(),
        year: z.number().int().nonnegative(),
    });

export type Meeting = z.infer<typeof meetingSchema>;