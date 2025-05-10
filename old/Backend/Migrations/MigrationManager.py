import glob
import os
import sqlite3
import sys

STOIC_MIGRATION_UP_STR = "-- StoicMigration Up\n"
STOIC_MIGRATION_DOWN_STR = "-- StoicMigration Down\n"


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
    if mode == "up":
        if up_index < down_index:
            migration_lines = lines[up_index + 1:down_index]
        else:
            migration_lines = lines[up_index + 1:len(lines)]
    else:
        if down_index < up_index:
            migration_lines = lines[down_index + 1:up_index]
        else:
            migration_lines = lines[down_index + 1:len(lines)]

    found_index = 0
    for i in range(len(migration_lines)):
        migration_line = migration_lines[i]
        if delimiter in migration_line:
            ret_migrations.append("".join(migration_lines[found_index:i + 1]))
            found_index = i + 1

    return ret_migrations


if __name__ == "__main__":
    DIR: str = "./Backend/Migrations"
    EXTENSION: str = ".sql"

    if len(sys.argv) != 2 or sys.argv[1] not in ["up", "down"]:
        print("Usage: <script> up|down")
        exit(-1)

    migration_mode = sys.argv[1]
    conn = sqlite3.connect('./Backend/Database/AuroraAlert.db')
    cursor = conn.cursor()

    files = get_files_by_extension(DIR, EXTENSION)
    for file in files:
        if migration_mode == "up":
            print(f"Migration Up: {file}")
        else:
            print(f"Migration Down: {file}")
        migrations = getMigrationsFromFile(file, migration_mode)
        for migration in migrations:
            cursor.execute(migration)

    conn.close()
