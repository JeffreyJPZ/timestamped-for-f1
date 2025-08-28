import z from "zod";

const eventCategory = z
    .enum([
        "driver-action",
        "driver-notification",
        "sector-notification",
        "track-notification",
        "session-notification",
        "other"
    ]);

const eventCause = z
    .enum([
        "personal-best-lap",
        "incident",
        "track-limits",
        "out",
        "overtake",
        "pit",
        "black-flag",
        "black-and-orange-flag",
        "black-and-white-flag",
        "blue-flag",
        "incident-verdict",
        "provisional-classification",
        "qualifying-stage-classification",
        "green-flag",
        "yellow-flag",
        "double-yellow-flag",
        "chequered-flag",
        "red-flag",
        "safety-car-deployed",
        "virtual-safety-car-deployed",
        "safety-car-ending",
        "virtual-safety-car-ending",
        "session-start",
        "session-end",
        "session-stop",
        "session-resume",
        "practice-start",
        "practice-end",
        "q1-start",
        "q1-end",
        "q2-start",
        "q2-end",
        "q3-start",
        "q3-end",
        "race-start",
        "race-end",
        "race-control-message"
    ]);

const eventRole = z
    .enum([
        "initiator",
        "participant"
    ]);

const tyreCompound = z
    .enum([
        "SOFT",
        "MEDIUM",
        "HARD",
        "INTERMEDIATE",
        "WET"
    ]);

export const eventSchema = z
    .object({
        category: eventCategory,
        cause: eventCause,
        date: z.iso.datetime(),
        details: z
            .object({
                lap_number: z.number().int().positive().nullish(),
                marker: z
                    .union([
                        z.string(),
                        z.object({
                            x: z.number(),
                            y: z.number(),
                            z: z.number()
                        })
                    ])
                    .nullish(),
                driver_roles: z.record(z.string(), eventRole).nullish(),
                position: z.number().int().positive().nullish(),
                lap_duration: z.number().nonnegative().nullish(),
                verdict: z.string().nullish(),
                reason: z.string().nullish(),
                message: z.string().nullish(),
                compound: tyreCompound.nullish(),
                tyre_age_at_start: z.number().int().nonnegative().nullish(),
                pit_lane_duration: z.number().nonnegative().nullish(),
                pit_stop_duration: z.number().nonnegative().nullish(),
                qualifying_stage_number: z.union([z.literal(1), z.literal(2)]).nullish(),
                eliminated: z.boolean().nullish(),
            })
            .nullish(),
        meeting_key: z.number().int().positive(),
        session_key: z.number().int().positive()
    });

export type Event = z.infer<typeof eventSchema>;
export type EventCategory = z.infer<typeof eventCategory>;
export type EventCause = z.infer<typeof eventCause>;
export type EventRole = z.infer<typeof eventRole>;
export type TyreCompound = z.infer<typeof tyreCompound>;