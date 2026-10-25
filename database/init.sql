-- init.sql: goals, actions, and a daily rollup view
 
CREATE TABLE IF NOT EXISTS goals (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  -- 1, 2, 3, ...
    goal_name    TEXT        NOT NULL,
    record_start TIMESTAMPTZ NOT NULL DEFAULT now(),
    record_end   TIMESTAMPTZ,                                       -- NULL = still tracking
    CONSTRAINT goals_record_range_chk
        CHECK (record_end IS NULL OR record_end >= record_start)
);
 
CREATE TABLE IF NOT EXISTS actions (
    goal_id INTEGER     NOT NULL REFERENCES goals (id) ON DELETE CASCADE,
    time    TIMESTAMPTZ NOT NULL DEFAULT now()
);
 
CREATE INDEX IF NOT EXISTS actions_goal_id_time_idx
    ON actions (goal_id, time);
 
-- One row per goal per calendar day on which it was completed at least once.
-- Days are bucketed in NZ local time so late-night actions land on the right day.
CREATE OR REPLACE VIEW daily_actions AS
SELECT DISTINCT
    g.goal_name,
    (a.time AT TIME ZONE 'Pacific/Auckland')::date AS day_completed
FROM actions AS a
JOIN goals   AS g ON g.id = a.goal_id;
 