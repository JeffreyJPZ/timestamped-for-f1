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

const marshalSectorSchema = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("marshal-sector")
    });

const miniSectorSchema = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("mini-sector")
    });

const turnSchema = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("turn")
    });

export type Circuit = z.infer<typeof circuitSchema>;
export type CircuitLocationType = z.infer<typeof circuitLocationType>;
export type MarshalSector = z.infer<typeof marshalSectorSchema>;
export type MiniSector = z.infer<typeof miniSectorSchema>;
export type Turn = z.infer<typeof turnSchema>;