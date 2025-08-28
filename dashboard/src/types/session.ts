import z from "zod";

const sessionName = z
    .enum([
        "Practice 1",
        "Practice 2",
        "Practice 3",
        "Sprint Shootout", // Sprint Qualifying name pre-2024
        "Sprint Qualifying",
        "Qualifying",
        "Sprint",
        "Race"
    ]);

const sessionType = z
    .enum([
        "Practice",
        "Qualifying",
        "Race"
    ]);

const sessionSchema = z
    .object({
        circuit_key: z.number().int().positive(),
        circuit_short_name: z.string(),
        country_code: z.string().length(3),
        country_key: z.number().int().positive(),
        country_name: z.string(),
        date_start: z.iso.datetime(),
        date_end: z.iso.datetime(),
        gmt_offset: z.string().regex(/^[-+]\d{2}:\d{2}:\d{2}$/),
        location: z.string(),
        meeting_key: z.number().int().positive(),
        session_key: z.number().int().positive(),
        session_name: sessionName,
        session_type: sessionType,
        year: z.number().int().nonnegative(),
    });

export type Session = z.infer<typeof sessionSchema>;
export type SessionName = z.infer<typeof sessionName>;
export type SessionType = z.infer<typeof sessionType>;