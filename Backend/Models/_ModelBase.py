import sqlite3


class ModelBase:
    def create(self, conn):
        # Extract instance attributes dynamically (excluding private/protected ones)
        members = {key: value for key, value in self.__dict__.items() if
                   not key.startswith("_") and not key.startswith("id")}

        placeholders = []
        for key in members.keys():
            placeholders.append(f"{key} = ?")

        keys_implode = ", ".join(members.keys())

        values = []
        for key in members.keys():
            if isinstance(members[key], str):
                values.append(f"\"{members[key]}\"")
            else:
                values.append(str(members[key]))

        values_implode = ", ".join(values)

        sql = f"INSERT INTO {self.__class__.__name__} ({keys_implode}) VALUES ({values_implode});"
        cursor = conn.cursor()

        cursor.execute(sql)

        if self.__dict__.get("id") is not None:
            self.id = cursor.lastrowid

        conn.commit()

    def read(self, conn):
        pass

    def update(self, conn):
        pass

    def delete(self, conn):
        pass

    def __getitem__(self, x):
        return self.__dict__[x]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)
