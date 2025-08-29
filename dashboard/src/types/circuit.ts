import z from "zod";

export const circuitLocationType = z
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

export const circuit = z
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

export const circuitRead = circuit
    .pick({
        circuit_key: true,
        year: true
    });

export const marshalSector = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("marshal-sector")
    });

export const marshalSectorRead = marshalSector
    .pick({
        number: true
    })
    .extend(
        circuit.pick({
            circuit_key: true,
            year: true
        })
        .shape
    );

export const miniSector = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("mini-sector")
    });

export const miniSectorRead = miniSector
    .pick({
        number: true
    })
    .extend(
        circuit.pick({
            circuit_key: true,
            year: true
        })
        .shape
    );

export const turn = z
    .object({
        ...circuitLocation.shape,
        type: z.literal("turn")
    });

export const turnRead = turn
    .pick({
        number: true
    })
    .extend(
        circuit.pick({
            circuit_key: true,
            year: true
        })
        .shape
    );

export type CircuitLocationType = z.infer<typeof circuitLocationType>;

export type Circuit = z.infer<typeof circuit>;
export type CircuitRead = z.infer<typeof circuitRead>;

export type MarshalSector = z.infer<typeof marshalSector>;
export type MarshalSectorRead = z.infer<typeof marshalSectorRead>;

export type MiniSector = z.infer<typeof miniSector>;
export type MiniSectorRead = z.infer<typeof miniSectorRead>;

export type Turn = z.infer<typeof turn>;
export type TurnRead = z.infer<typeof turnRead>;