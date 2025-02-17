CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    channel_name TEXT NOT NULL,
    kp_index_threshold REAL NOT NULL,
    cloud_coverage_threshold INTEGER NOT NULL
)