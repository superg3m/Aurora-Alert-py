# 'target_time': time(13, 0),


class GuildModel:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.start_time: int = 14  # 24-hour format
        self.end_time: int = 21
        self.channel_name: str = "aurora-alert"
        self.kp_index_threshold: float = 4.67
        self.cloud_coverage_threshold: int = 35
        self.time_zone = "EST"
        self.moon_phase_blacklist: str = "Full Moon,Waxing Gibbous,Waning Gibbous"  # Comma separated values

    def __getitem__(self, x):
        return self.__dict__[x]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def update(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE guilds 
            SET name = ?, start_time = ?, end_time = ?, channel_name = ?, kp_index_threshold = ?, cloud_coverage_threshold = ? 
            WHERE id = ?
        """, (self.__dict__.values()))
        conn.commit()

    @staticmethod
    def from_id(conn, guild_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold 
            FROM guilds WHERE id = ?
        """, (guild_id,))

        row = cursor.fetchone()
        if row:
            guild = GuildModel()
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
            guild = GuildModel()
            (
                guild.id, guild.name, guild.start_time, guild.end_time,
                guild.channel_name, guild.kp_index_threshold, guild.cloud_coverage_threshold
            ) = row

            ret.append(guild)

        return ret

    def create(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO guilds (name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (*self.__dict__.values(),))
        conn.commit()

        guild = GuildModel()
        guild.id = cursor.lastrowid

        return guild


if __name__ == "__main__":
    a = GuildModel()
    print(*a.__dict__.values())
