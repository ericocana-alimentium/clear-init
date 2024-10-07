# %%
from models.db_connection import DBConnection

class BaseController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.db_connected = False

    def connect_to_db(self):
        if not self.db_connected:
            self.db = DBConnection(self.db_name)
            self.db.connect()
            self.db_connected = True

    def close_db(self):
        if self.db_connected and self.db:
            self.db.close()
            self.db_connected = False




