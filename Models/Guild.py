class GuildConfig:
    def __init__(self, guild_id, name, age):
        self.name = name
        self.age = age






# 'target_time': time(13, 0),

class Guild:
    def __init__(self, guild_id, name, age):
        self.id: int = guild_id
        self.name: str = name
        self.start_time: int= 14  # from 1pm to 8pm or whatever in 24 hour time EST Assumed
        self.end_time: int=  21     # from 1pm to 8pm or whatever in 24 hour time EST Assumed
        self.channel_name: str =  "aurora-alert"
        self.kp_index_threshold: float = 4.67
        self.cloud_coverage_threshold: int = 35

        self.age = age

    def save(self, conn):
        """Save updated object back to the database."""
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (self.name, self.age, self.id))
        conn.commit()

    @staticmethod
    def get_by_id(conn, user_id):
        """Fetch a user by ID and return as an object."""
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, age FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(*row)  # Unpack row into User(id, name, age)
        return None

    @staticmethod
    def create(conn, name, age):
        """Create a new user and return the created object."""
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        return User(cursor.lastrowid, name, age)