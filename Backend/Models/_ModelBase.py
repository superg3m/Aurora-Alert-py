class ModelBase:
    def create(self):
        # Extract instance attributes dynamically (excluding private/protected ones)
        print(self.__dict__.items())
        attributes = {key: value for key, value in self.__dict__.items() if not key.startswith("_")}

        set_clause = ", ".join(f"{col} = ?" for col in attributes.keys() if col != "id")
        values = tuple(attributes[col] for col in attributes.keys() if col != "id")

        sql = f"UPDATE {self.__class__.__name__.lower()}s SET {set_clause} WHERE id = ?"

        print(sql)

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
