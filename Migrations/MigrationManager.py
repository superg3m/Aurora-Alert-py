import sqlite3
import sys


class MigrationManager:
    def __init__(self, migration_dir: str, extension: str):
        self.migration_dir: str = migration_dir
        self.extension: str = extension
        self.migrations: list[str] = []

    def getMigrations(self, migration_mode):
        if migration_mode == "up":

        elif migration_mode == "down":

        else:
            exit(-1)

    def executeMigrations(self, cursor):
        for migration in self.migrations:
            cursor.execute(migration)



if __name__ == "__main__":
    DIR: str = "./Migrations"
    EXTENSION: str = ".sql"
    manager = MigrationManager(DIR, EXTENSION)

    if len(sys.argv) != 2 or sys.argv[1] not in ["up", "down"]:
        print("Usage: <script> up|down")
        exit(-1)


    migration_mode = sys.argv[1]

    conn = sqlite3.connect('./Database/guild.db')
    cursor = conn.cursor()

    migration_mode

    manager.executeMigrations(cursor, migration_mode)

    conn.close()




