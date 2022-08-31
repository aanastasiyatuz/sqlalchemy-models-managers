import sqlalchemy
from sqlalchemy.sql import text as SQL
from decouple import config

class Connect:
    def __enter__(self):
        # print("\033[5mconnect to database\033[0m")

        self.engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=config("DB_USERNAME"),
                password=config("DB_PASSWORD"),
                database=config("DATABASE")
            )
        )

        self.connection = self.engine.connect()
        return self
    
    def __exit__(self, *args, **kwargs):
        self.connection.close()
    
    def run(self, command):
        if not self.connection.closed:
            print(f"run \033[91m{command}\033[0m")
            return self.connection.execute(SQL(command))
        raise Exception("Closed connection")
