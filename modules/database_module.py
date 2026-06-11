import mysql.connector
from datetime import datetime
class DatabaseModule:

    print("DATABASE MODULE LOADED")
    def __init__(self):

        print("DatabaseModule constructor")

        self.conn = None
        self.cursor = None

        response = self.connect()

        print("Connection Response:", response)
        print("Conn =", self.conn)
        print("Cursor =", self.cursor)
    def connect(self):

        try:

            self.conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="1Satyam112@",
                database="sanima_bot"
            )

            self.cursor = self.conn.cursor()

            return "Success"

        except Exception as e:

            print("Connection Error:", str(e))

            return str(e)

    def insert_logs(self,status,message):
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO logs(timestamp, level, message)
            VALUES (%s, %s, %s)
            """

        values = (
            currentTime,
            status,
            message
        )

        self.cursor.execute(sql, values)

        self.conn.commit()
    def read(self):

        print("Inside read()")
        print("self =", self)
        print("conn =", self.conn)
        print("cursor =", self.cursor)

        sql = """
        SELECT * FROM logs
        """

        self.cursor.execute(sql)

        return self.cursor.fetchall()
    