from modules.database_module import DatabaseModule
from datetime import datetime
class LogModule:

    def __init__(self):

        self.database = DatabaseModule()
        self.database.connect()

    def success(self, msg):
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try: 
            self.database.insert_logs(
                "SUCCESS",
                msg
            )
        except Exception as e:
            print("Error inserting in the database", str(e))

    def error(self, msg):
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.database.insert_logs(
                "ERROR",
                msg
            )
        except Exception as e:
            print("Error inserting in the database", str(e))