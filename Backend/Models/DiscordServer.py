# 'target_time': time(13, 0),
import sqlite3

from Backend.Models._ModelBase import ModelBase


class DiscordServer(ModelBase):
    def __init__(self):

        self.id: int = 0
        self.name: str = "TESINGS"
        self.start_time: int = 14  # 24-hour format
        self.end_time: int = 21
        self.channel_name: str = "aurora-alert"
        self.time_zone = "EST"
        self.kp_index_threshold: float = 4.67
        self.cloud_coverage_percentage_threshold: int = 35
        self.moon_phase_blacklist: str = "Full Moon,Waxing Gibbous,Waning Gibbous"  # comma separated values

    @staticmethod
    def from_id(conn, guild_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold 
            FROM guilds WHERE id = ?
        """, (guild_id,))

        row = cursor.fetchone()
        if row:
            guild = DiscordServer()
            (
                guild.id, guild.name, guild.start_time, guild.end_time,
                guild.channel_name, guild.kp_index_threshold, guild.cloud_coverage_threshold
            ) = row
            return guild

        return None

    @staticmethod
    def get_all_guilds_data(conn):
        """Fetch a guild by ID and return as an object."""
        cursor = conn.cursor()
        cursor.execute("""SELECT *  FROM guilds""")
        row = cursor.fetchone()

        ret = []
        for row in cursor:
            guild = DiscordServer()
            (
                guild.id, guild.name, guild.start_time, guild.end_time,
                guild.channel_name, guild.kp_index_threshold, guild.cloud_coverage_threshold
            ) = row

            ret.append(guild)

        return ret


if __name__ == "__main__":
    try:
        conn = sqlite3.connect('../Database/AuroraAlert.db')

        a = DiscordServer()
        a.create(conn)

        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
