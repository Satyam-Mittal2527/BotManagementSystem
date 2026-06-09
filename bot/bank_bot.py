from BotManagement.models import DatabaseModule
from modules.log_module import LogModule
from datetime import datetime
import subprocess
import psutil
import threading
import os
        
        
project_root = "/home/satyammittal/SanimaBots"

class Database:

    def __init__(self):

        print("BankBot constructor")

        self.database = DatabaseModule()

        self.logger = LogModule()
   
    def Add_bot(self, package):
        response = self.database.insert_bot(package)
        return response
        
    def get_bots(self):

        response = self.database.get_bots()
        print(response)
        return response

    def view_runs(self, botId):
        
        response = self.database.view_runs(botId)

        return response

    def view_logs(self, runId):

        response = self.database.view_logs(runId)

        return response
    def get_bot_by_name(self, bot_name):

        response = self.database.get_bot_by_name(bot_name)

        return response
    def get_bot_code(self, bot_name):

        bot = self.get_bot_by_name(bot_name)

        if "script_path" not in bot:
            return bot

        file_path = os.path.join(
            bot["script_path"],
            "main.py"
        )

        try:

            with open(file_path, "r") as file:
                code = file.read()

            return {
                "status": "success",
                "code": code
            }

        except Exception as e:

            return {
                "status": "error",
                "description": str(e)
            }


class Bot:
    def __init__(self):

        print("Running Bot")


        self.database = DatabaseModule()

    def monitor_process(self, process, botId, runID):
        try:
            for line in process.stdout:
                print(line, end='')  

                print(self.database.insert_logs(
                    runID,
                    {
                        "status": "INFO",
                        "message": line.strip()
                    }
                ))

            process.wait()

            if process.returncode == 0:
                self.database.insert_logs(
                    runID,
                    {
                        "status": "Stopped",
                        "message": "Bot completed successfully"
                    }
                )
                updateBot = self.database.updateColumns(
                    botId,
                    process.pid,
                    "INACTIVE"
                )
                insertRuns = self.database.update_run(
                    runID,
                    "COMPLETED"
                )

                return "Completed process"
            else:
                error = process.stderr.read()
                print("Error ocuured during stop",error)
                self.database.insert_logs(
                    runID,
                    {
                        "status": "Stooped",
                        "message": str(e)
                    }
                )
                insertRuns = self.database.update_run(
                    runID,
                    "STOPPED"
                )
                updateBot = self.database.updateColumns(
                    botId,
                    process.pid,
                    "INACTIVE"
                )
                return "Completed with error"
        except Exception as e:
            print("Bank bot: error:",str(e))
    def run_bot(self, botPack):

        botId = botPack["botId"]

        bot = self.database.get_bot_toRun(botId)

        env = os.environ.copy()
        env["PYTHONPATH"] = project_root

        process = subprocess.Popen(
                ["python", "-u", "main.py"],
                cwd=bot["script_path"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env
            )
        try:
            runID = self.database.insert_runs(
                botId,
                "RUNNING"
            )

            threading.Thread(
                target=self.monitor_process,
                args=(process, botId, runID),
            ).start()

            updateBot = self.database.updateColumns(
                botId,
                process.pid,
                "ACTIVE"
            )

            

            update_logs = self.database.insert_logs(
                runID,
                {
                    "status": "Running",
                    "message": "Bot is currently Running"
                }
            )
            return {
                "status": "Running",
                "description": "Bot Started Successfully",
                "pid": process.pid
            }

        except Exception as e:
            update_logs = self.database.insert_logs(
                runID,
                {
                    "status": "Error",
                    "message": str(e)
                }
            )
            print("INSERTIG RUN CODE")
            updateBot = self.database.updateColumns(
                botId,
                process.pid,
                "ERROR"
            )
            return {
                "status": "Error",
                "description": str(e)
            }
    def stop_bot(self, botPack):
        print("bankVbot stop call")
        botId = botPack["botId"]
        try:
            bot = self.database.get_bot_toRun(botId)
            
            pid = bot["pid"]
            print("Pid found",pid)

           
            
            process = psutil.Process(pid)
            process.terminate()
            print("Process Terminatewd")
            updateBot = self.database.updateColumns(
                botId,
                pid,
                "INACTIVE"
            )
            runID = self.database.insert_runs(
                botId,
                "STOPPED BY USER"
            )
            insertRuns = self.database.update_run(
                    runID,
                    "STOPPED BY USER"
                )
            update_logs = self.database.insert_logs(
                runID,
                {
                    "status": "Stooped BY USER",
                    "message": "Bot was stopped by the user"
                }
            )

            print("Returned from database model",updateBot)
            return {
                "status": "stopped",
                "description": "Bot Stopped Successfully",
                "pid": process.pid
            }

        except Exception as e:
            update_logs = self.database.insert_logs(
                botId,
                {
                    "status": "Error",
                    "message": str(e)
                }
            )

            return {
                "status": "Error",
                "description": str(e)
            }
