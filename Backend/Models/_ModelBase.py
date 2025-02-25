class ModelBase:
    def create(self, conn):
        cursor = conn.cursor()

        

        sql = f"""
            UPDATE guilds 
            SET name = ?, start_time = ?, end_time = ?, channel_name = ?, kp_index_threshold = ?, cloud_coverage_threshold = ? 
            WHERE id = ?
        """
        cursor.execute(sql, (self.__dict__.values()))
    def read(self, conn):
    def update(self, conn):
    def delete(self, conn):
    def __getitem__(self, x):
        return self.__dict__[x]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)