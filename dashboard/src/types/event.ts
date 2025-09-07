import z from "zod";

export const eventCategory = z
    .enum([
        "driver-action",
        "driver-notification",
        "sector-notification",
        "track-notification",
        "session-notification",
        "other"
    ]);

export const eventCause = z
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

export const eventRole = z
    .enum([
        "initiator",
        "participant"
    ]);

export const tyreCompound = z
    .enum([
        "SOFT",
        "MEDIUM",
        "HARD",
        "INTERMEDIATE",
        "WET",
        "UNKNOWN"
    ]);

const eventDetails = z
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
    });

export const event = z
    .object({
        category: eventCategory,
        cause: eventCause,
        date: z.iso.datetime({ offset: true }),
        elapsed_time: z.string().regex(/^(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?$/),
        details: eventDetails.nullish(),
        meeting_key: z.number().int().nonnegative(),
        session_key: z.number().int().nonnegative()
    });

export const events = z.array(event);

export const eventsRead = event
    .omit({
        // Not compatible with events API, need to implement some other way
        details: true,
    })
    .extend({
        category: z.array(eventCategory),
        cause: z.array(eventCause),
        date: z.array(z.iso.datetime({ offset: true })),
        elapsed_time: z.array(z.string().regex(/^(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?$/)),
        meeting_key: z.array(z.number().int().positive()),
        session_key: z.array(z.number().int().positive())
    })
    .partial();

export type EventCategory = z.infer<typeof eventCategory>;
export type EventCause = z.infer<typeof eventCause>;
export type EventRole = z.infer<typeof eventRole>;
export type TyreCompound = z.infer<typeof tyreCompound>;

export type Event = z.infer<typeof event>;
export type Events = z.infer<typeof events>;
export type EventsRead = z.infer<typeof eventsRead>;