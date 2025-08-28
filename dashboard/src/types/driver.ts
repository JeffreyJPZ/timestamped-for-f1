import z from "zod";

const driverSchema = z
    .object({
        broadcast_name: z.string(),
        country_code: z.string().length(3),
        driver_number: z.number().int().positive(),
        first_name: z.string(),
        full_name: z.string(),
        headshot_url: z.url(),
        last_name: z.string(),
        meeting_key: z.number().int().positive(),
        name_acronym: z.string().max(3),
        session_key: z.number().int().positive(),
        team_colour: z.string().regex(/^[A-Fa-f0-9]{6}$/), // Hex colour
        team_name: z.string(),
    });

export type Driver = z.infer<typeof driverSchema>;