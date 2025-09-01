import z from "zod";

export const meeting = z
    .object({
        circuit_key: z.number().int().nonnegative(),
        circuit_short_name: z.string(),
        country_code: z.string().length(3),
        country_key: z.number().int().nonnegative(),
        country_name: z.string(),
        date_start: z.iso.datetime({ offset: true }),
        gmt_offset: z.string().regex(/^-?\d{2}:\d{2}:\d{2}$/),
        location: z.string(),
        meeting_key: z.number().int().nonnegative(),
        meeting_name: z.string(),
        meeting_official_name: z.string(),
        year: z.number().int().nonnegative(),
    });

export const meetings = z.array(meeting);

export const meetingRead = meeting
    .pick({
        meeting_key: true
    });

export const meetingsRead = meeting
    .extend({
        circuit_key: z.array(z.number().int().nonnegative()),
        circuit_short_name: z.array(z.string()),
        country_code: z.array(z.string().length(3)),
        country_key: z.array(z.number().int().nonnegative()),
        country_name: z.array(z.string()),
        date_start: z.array(z.iso.datetime({ offset: true })),
        gmt_offset: z.array(z.string().regex(/^-?\d{2}:\d{2}:\d{2}$/)),
        location: z.array(z.string()),
        meeting_key: z.array(z.number().int().nonnegative()),
        meeting_name: z.array(z.string()),
        meeting_official_name: z.array(z.string()),
        year: z.array(z.number().int().nonnegative()),
    })
    .partial();

export type Meeting = z.infer<typeof meeting>;
export type Meetings = z.infer<typeof meetings>;
export type MeetingRead = z.infer<typeof meetingRead>;
export type MeetingsRead = z.infer<typeof meetingsRead>;