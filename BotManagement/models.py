from django.db import models
import mysql.connector
from datetime import datetime

import mysql.connector
    
class DatabaseModule:
    def __init__(self):
       pass
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1Satyam112@",
            database="sanima_bot"
        )
    def insert_bot(self, package):
        conn = self.get_connection()
        cursor = conn.cursor()
        print("Insert Bot Database models ")
        first_name = package["first_name"]
        last_name = package["last_name"]
        bot_name = package["bot_name"]
        branch = package["branch"]
        status = package["status"]
        script_path = package["script_path"]

        sql = """
            INSERT INTO BOTS
            (
                first_name,
                last_name,
                bot_name,
                branch,
                status,
                script_path
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            first_name,
            last_name,
            bot_name,
            branch,
            status,
            script_path
        )

        try:
            cursor.execute(sql, values)
            conn.commit()

            return "New Bot Added"

        except Exception as e:
            print("Error inserting bot:", str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def delete_bots(self, botName):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM BOTS WHERE 
            bot_name = %s
        """

        try:
            cursor.execute(sql, (botName,))
            conn.commit()

            return "Deleted Bot"
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
            conn.close()      
    def get_bot_toRun(self, botId):

        conn = self.get_connection()
        cursor = conn.cursor()

        print("Reached Database Models")

        sql = """
        SELECT script_path, pid
        FROM BOTS
        WHERE id = %s
        """

        cursor.execute(sql, (botId,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:

            raise Exception(
                f"Bot {botId} not found in database"
            )

        return {

            "script_path": row[0],

            "pid": row[1]

        }
            
    def get_bots(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql= """
            SELECT id,bot_name, status , branch, created_at 
            FROM BOTS
        
        """
        try:
      
            cursor.execute(sql)

            return cursor.fetchall()
        except Exception as e:
            print(str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def get_active_bots(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT COUNT(*) FROM BOTS WHERE
            status = "ACTIVE"
        """
        try:
      
            cursor.execute(sql)

            return cursor.fetchone()
        except Exception as e:
            print(str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def get_inactive_bots(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT COUNT(*) FROM BOTS WHERE
            status = "INACTIVE"
        """
        try:
      
            cursor.execute(sql)

            return cursor.fetchone()
        except Exception as e:
            print(str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def updateColumns(self, botId, pid, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE BOTS
            SET status = %s,
                pid = %s
            WHERE id = %s
        """

        try:

            cursor.execute(sql, (status, pid, botId))
            conn.commit()

            return "Updated database"

        except Exception as e:
            print("Error in the database model", str(e))
            return str(e)

        finally:
            cursor.close()
            conn.close()
            
    def insert_logs(self, runId, log_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        print("Insert Logs in the database models reached")
      
        status = log_data["status"]
        message  = log_data["message"]

        sql = """
                INSERT INTO BOT_LOGS
                (
                    run_id,
                    status,
                    message
                )
                VALUES (%s, %s, %s)

            """

        values = (
                runId,
                status,
                message
            )

        try:
            cursor.execute(sql, values)
            conn.commit()
            print("Logs Added")
            return "Logs Added"

        except Exception as e:
            print("Error inserting logs:", str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def delete_logs(self, runId):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM BOT_LOGS WHERE 
            run_id = %s
        """

        try:
            cursor.execute(sql, (runId,))
            conn.commit()

            return "Deleted Logs"
        except Exception as e:
            print(str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def view_runs(self, botId):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM BOT_RUNS 
        WHERE bot_id = %s
        """

        try:
            cursor.execute(sql, (botId,))

            rows = cursor.fetchall()

            logs = []
            print(rows)
            for row in rows:
                logs.append({
                    "id": row[0],
                    "bot_id": row[1],
                    "started_at": row[2],
                    "ended_at" : row[3],
                    "status": row[4]
                })

            return {
                "bots": logs
            }

        except Exception as e:
            print(str(e))
            return {
                "bots": [],
                "error": str(e)
            }
        finally:
            cursor.close()
            conn.close()
            
    def insert_runs(self, botId, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        print("Inserting runs")
        sql = """
            INSERT INTO BOT_RUNS
            (
            bot_id,
            status
            ) 
            VALUES (%s, %s)
        
        """

        values = (
            botId,
            status
        )
        try:
            cursor.execute(sql, values)
            conn.commit()

            return cursor.lastrowid
        except Exception as e:
            print("Error inserting Run", str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
    def delete_runs(self, botId):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM BOT_RUNS WHERE 
            bot_id = %s
        """

        try:
            cursor.execute(sql, (botId,))
            conn.commit()

            return "Deleted Runs"
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
            conn.close()  
    def update_run(self, runID, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        print("Reached Update run")
        ended_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = """
            UPDATE BOT_RUNS SET
            status = %s,
            ended_at = %s
            WHERE id = %s
        """

        try:
            cursor.execute(sql, (status, ended_at, runID ))
            conn.commit()

            return "UpdatedRuns"
        except Exception as e:
            print("Error in the database runs model", str(e))
            return str(e)
        finally:
            cursor.close()
            conn.close()
            
    def view_logs(self, runId):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM BOT_LOGS
        WHERE run_id = %s
        """

        try:

            cursor.execute(sql, (runId,))

            rows = cursor.fetchall()

            logs = []

            for row in rows:
                logs.append({
                    "id": row[0],
                    "run_id": row[1],
                    "status": row[2],
                    "message" : row[3],
                    "created_at": row[4]
                })
            return {
                "bots": logs
            }
        except Exception as e:
            return {
                "bots": [],
                "error": str(e)
            }
        finally:
            cursor.close()
            conn.close()

    def get_bot_by_name(self,bot_name):

        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT
                id,
                bot_name,
                branch,
                status,
                script_path
            FROM BOTS
            WHERE bot_name = %s
        """

        try:

            cursor.execute(
                sql,
                (bot_name,)
            )

            row = cursor.fetchone()

            if row is None:

                return {
                    "status": "Error",
                    "description": "Bot not found"
                }

            return row

        except Exception as e:

            return {
                "status": "Error",
                "description": str(e)
            }

        finally:

            cursor.close()
            conn.close()
    def get_full_botDetails(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT id, first_name, last_name, bot_name, branch, created_at FROM BOTS
        """

        try:

            cursor.execute(
                sql
            )

            row = cursor.fetchall()

            if row is None:

                return {
                    "status": "Error",
                    "description": "details not found"
                }

            return row

        except Exception as e:

            return {
                "status": "Error",
                "description": str(e)
            }

        finally:

            cursor.close()
            conn.close()


                