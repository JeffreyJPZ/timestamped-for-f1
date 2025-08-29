import z from "zod";

export const sessionName = z
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

export const sessionType = z
    .enum([
        "Practice",
        "Qualifying",
        "Race"
    ]);

export const session = z
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

export const sessionRead = session
    .pick({
        session_key: true
    });

export const sessionsRead = session
    .extend({
        circuit_key: z.array(z.number().int().positive()),
        circuit_short_name: z.array(z.string()),
        country_code: z.array(z.string().length(3)),
        country_key: z.array(z.number().int().positive()),
        country_name: z.array(z.string()),
        date_start: z.array(z.iso.datetime()),
        date_end: z.array(z.iso.datetime()),
        gmt_offset: z.array(z.string().regex(/^[-+]\d{2}:\d{2}:\d{2}$/)),
        location: z.array(z.string()),
        meeting_key: z.array(z.number().int().positive()),
        session_key: z.array(z.number().int().positive()),
        session_name: z.array(sessionName),
        session_type: z.array(sessionType),
        year: z.array(z.number().int().nonnegative()),
    })
    .partial();

export type SessionName = z.infer<typeof sessionName>;
export type SessionType = z.infer<typeof sessionType>;

export type Session = z.infer<typeof session>;
export type SessionRead = z.infer<typeof sessionRead>;
export type SessionsRead = z.infer<typeof sessionsRead>;