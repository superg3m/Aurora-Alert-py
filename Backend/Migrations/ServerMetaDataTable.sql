-- StoicMigration Up
CREATE TABLE IF NOT EXISTS ServerMetaData (
    id INTEGER PRIMARY KEY,
    daily_open_weather_api_calls INT NOT NULL
);

-- StoicMigration Down
DROP TABLE IF EXISTS ServerMetaData;