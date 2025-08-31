import z from "zod";

export const driver = z
    .object({
        broadcast_name: z.string(),
        country_code: z.string().length(3),
        driver_number: z.number().int().positive(),
        first_name: z.string(),
        full_name: z.string(),
        headshot_url: z.url().nullable(),
        last_name: z.string(),
        meeting_key: z.number().int().positive(),
        name_acronym: z.string().max(3),
        session_key: z.number().int().positive(),
        team_colour: z.string().regex(/^[A-Fa-f0-9]{6}$/), // Hex colour
        team_name: z.string(),
    });

export const drivers = z.array(driver);

export const driverRead = driver
    .pick({
        driver_number: true,
        meeting_key: true,
        session_key: true
    });

export const driversRead = driver
    .extend({
        broadcast_name: z.array(z.string()),
        country_code: z.array(z.string().length(3)),
        driver_number: z.array(z.number().int().positive()),
        first_name: z.array(z.string()),
        full_name: z.array(z.string()),
        headshot_url: z.array(z.url()),
        last_name: z.array(z.string()),
        meeting_key: z.array(z.number().int().positive()),
        name_acronym: z.array(z.string().max(3)),
        session_key: z.array(z.number().int().positive()),
        team_colour: z.array(z.string().regex(/^[A-Fa-f0-9]{6}$/)),
        team_name: z.array(z.string()),
    })
    .partial();

export type Driver = z.infer<typeof driver>;
export type Drivers = z.infer<typeof drivers>;
export type DriverRead = z.infer<typeof driverRead>;
export type DriversRead = z.infer<typeof driversRead>;