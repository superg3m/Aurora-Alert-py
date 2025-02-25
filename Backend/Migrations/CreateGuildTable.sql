-- StoicMigration Up
CREATE TABLE IF NOT EXISTS DiscordServer (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    channel_name TEXT NOT NULL,
    time_zone TEXT NOT NULL,
    kp_index_threshold REAL NOT NULL,
    cloud_coverage_percentage_threshold INTEGER NOT NULL,
    moon_phase_blacklist TEXT NOT NULL
);

-- StoicMigration Down
DROP TABLE IF EXISTS DiscordServer;
DROP TABLE IF EXISTS Guild;