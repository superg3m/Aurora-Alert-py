class Guild:
    def __init__(self, guild_id, name: str, start_time=14, end_time=21, channel_name="aurora-alert", kp_index_threshold=4.67, cloud_coverage_threshold=35):
        self.id: int = guild_id
        self.name: str = name
        self.start_time: int = start_time  # 24-hour format (EST assumed)
        self.end_time: int = end_time
        self.channel_name: str = channel_name
        self.kp_index_threshold: float = kp_index_threshold
        self.cloud_coverage_threshold: int = cloud_coverage_threshold

    def update(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE guilds 
            SET name = ?, start_time = ?, end_time = ?, channel_name = ?, kp_index_threshold = ?, cloud_coverage_threshold = ? 
            WHERE id = ?
        """, (self.name, self.start_time, self.end_time, self.channel_name, self.kp_index_threshold, self.cloud_coverage_threshold, self.id))
        conn.commit()

    @staticmethod
    def get_all_guild_data(conn):
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Guild""")

        ret = []
        for row in cursor:
            guild = Guild(
                row[0],
                name=row[1],
                start_time=row[2],
                end_time=row[3],
                channel_name=row[4],
                kp_index_threshold=row[5],
                cloud_coverage_threshold=row[6]
            )
            ret.append(guild)

        cursor.close()
        return ret

    @staticmethod
    def get_by_id(conn, guild_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold 
            FROM guilds WHERE id = ?
        """, (guild_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Guild(*row)  # Unpack row into Guild(id, name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold)
        return None

    @staticmethod
    def create(conn, name, start_time=14, end_time=21, channel_name="aurora-alert", kp_index_threshold=4.67, cloud_coverage_threshold=35):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO guilds (name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold))
        conn.commit()
        cursor.close()
        return Guild(cursor.lastrowid, name, start_time, end_time, channel_name, kp_index_threshold, cloud_coverage_threshold)