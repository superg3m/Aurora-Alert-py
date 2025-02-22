import glob
import os
import sqlite3
import sys

STOIC_MIGRATION_UP_STR = "-- StoicMigration Up"
STOIC_MIGRATION_DOWN_STR = "-- StoicMigration Down"


def get_files_by_extension(directory, extension) -> list[str]:
    pattern = os.path.join(directory, f"*{extension}")
    return glob.glob(pattern)


def getMigrationsFromFile(migration_file, mode) -> list[str]:
    ret_migrations: list[str] = []
    migration_str = STOIC_MIGRATION_UP_STR if mode == "up" else STOIC_MIGRATION_DOWN_STR
    delimiter = ';'

    f = open(migration_file)
    lines = f.readlines()
    up_index = lines.index(STOIC_MIGRATION_UP_STR)
    down_index = lines.index(STOIC_MIGRATION_DOWN_STR)

    migration_lines: list[str] = []
    if up_index < down_index:
        migration_lines = lines[up_index:down_index]
    else:
        migration_lines = lines[down_index:up_index]

    found_index = 0
    for i in range(len(migration_lines)):
        migration_line = migration_lines[i]
        if delimiter in migration_line:
            ret_migrations.append("".join(migration_lines[found_index:i]))
            found_index = i

    return ret_migrations


if __name__ == "__main__":
    DIR: str = "./Migrations"
    EXTENSION: str = ".sql"

    if len(sys.argv) != 2 or sys.argv[1] not in ["up", "down"]:
        print("Usage: <script> up|down")
        exit(-1)

    migration_mode = sys.argv[1]
    conn = sqlite3.connect('./Database/guild.db')
    cursor = conn.cursor()

    files = get_files_by_extension(DIR, EXTENSION)
    for file in files:
        migrations = getMigrationsFromFile(file, migration_mode)
        for migration in migrations:
            cursor.execute(migration)

    conn.close()
