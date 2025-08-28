import z from "zod";

const circuitLocationType = z
    .enum([
        "marshal-sector",
        "mini-sector",
        "turn"
    ]);

const circuitLocation = z
    .object({
        angle: z.number(),
        coordinates: z
            .object({
                x: z.number(),
                y: z.number()
            }),
        length: z.number().nonnegative(),
        number: z.number().int().positive(),
        type: circuitLocationType
    });

const circuitSchema = z
    .object({
        circuit_key: z.number().int().positive(),
        circuit_name: z.string(),
        coordinates: z
            .array(
                z.object({
                    x: z.number(),
                    y: z.number()
                })
            ),
        country_code: z.string().length(3),
        country_key: z.number().int().positive(),
        country_name: z.string(),
        location: z.string(),
        marshal_sectors: z.array(circuitLocation),
        mini_sectors: z.array(circuitLocation),
        rotation: z.number(),
        turns: z.array(circuitLocation),
        year: z.number().int().nonnegative()
    });

export type Circuit = z.infer<typeof circuitSchema>;
export type CircuitLocationType = z.infer<typeof circuitLocationType>;