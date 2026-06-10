from django.shortcuts import render
from bot.bank_bot import Database
from bot.bank_bot import Bot
from django.http import JsonResponse
import json
import os
import shutil
from django.conf import settings



def home(request):
    return render(request, "bot_dashboard.html")
def addBot(request):
    print("Got called add_bot page")
    return render(request,"add_bot.html")
def botPage(request):
    bot = Database()

    bots = bot.get_bots()

    context = {
        "bots": bots
    }
    print("CONTEXT",context)
    return render(
        request,
        "bot_page.html",
        context
    )
def DeleteBotPage(request):
    deleted_path = settings.DELETED_BOT_STORAGE_PATH

    deleted_bots = []

    for item in os.listdir(deleted_path):
        full_path = os.path.join(deleted_path, item)

        if os.path.isdir(full_path):
            deleted_bots.append(item)

    print(deleted_bots)

    context = {
    "deleted_bots": deleted_bots
    }

    return render(request, "deleted_bots.html", context)
def ViewBotCode(request):

    try:

        data = json.loads(request.body)

        bot_name = data["bot_name"]

        bot = Database()

        response = bot.get_bot_code(bot_name)

        context = {
            "bot_name": bot_name,
            "files": response["files"],
            "code": response["code"],
            "selected_file": response["selected_file"]
        }

        return render(
            request,
            "ViewBot.html",
            context
        )

    except Exception as e:

        return render(
            request,
            "ViewBot.html",
            {
                "error": str(e)
            }
        )
def ViewFile(request):

    try:

        data = json.loads(request.body)

        bot_name = data["bot_name"]
        file_name = data["file_name"]

        bot = Database()

        bot_data = bot.get_bot_by_name(bot_name)

        if file_name.startswith("TestHelper/"):

            file_path = os.path.join(
                settings.BOT_STORAGE_PATH,
                file_name
            )

        else:

            file_path = os.path.join(
                bot_data["script_path"],
                file_name
            )

        with open(file_path, "r") as f:

            code = f.read()

        return JsonResponse(
            {
                "status": "success",
                "code": code
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "status": "error",
                "description": str(e)
            }
        )
def profilePage(request):
    return render(request, "profile.html")
def EditBotPage(request):
    return render(request, "EditBot.html")
def UserPage(request):
    return render(request, "users.html")
def EditBot(request):

    bot = Database()

    try:

        bot_name = request.POST["bot_name"]
        bot_code = request.POST["bot_code"]
        file_name = request.POST["file_name"]

        bots = bot.get_bot_by_name(bot_name)

        if "script_path" not in bots:

            return JsonResponse(
                {
                    "status": "error",
                    "description": bots["description"]
                }
            )

        if file_name.startswith("TestHelper/"):

            file_path = os.path.join(
                settings.BOT_STORAGE_PATH,
                file_name
            )

        else:

            file_path = os.path.join(
                bots["script_path"],
                file_name
            )

        with open(file_path, "w") as file:

            file.write(bot_code)

        return JsonResponse(
            {
                "status": "success"
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "status": "error",
                "description": str(e)
            }
        )


def NewBot(request):

    try:

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        bot_name = request.POST["bot_name"]
        branch = request.POST["branch"]
        status = request.POST["status"]

        upload_type = request.POST.get("upload_type")

        # Root folder for this bot
        bot_folder = os.path.join(
            settings.BOT_STORAGE_PATH,
            bot_name
        )

        os.makedirs(bot_folder, exist_ok=True)

        # ----------------------------
        # Save helper files
        # ----------------------------
        helper_files = request.FILES.getlist("helper_files")
        helper_paths = request.POST.getlist("helper_paths")

        for file, relative_path in zip(helper_files, helper_paths):

            save_path = os.path.join(
                bot_folder,
                relative_path
            )

            os.makedirs(
                os.path.dirname(save_path),
                exist_ok=True
            )

            with open(save_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # ----------------------------
        # Single Python file upload
        # ----------------------------
        if upload_type == "file":

            file = request.FILES["script_files"]

            destination_path = os.path.join(
                bot_folder,
                "main.py"
            )

            with open(destination_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # ----------------------------
        # Folder upload
        # ----------------------------
        elif upload_type == "folder":

            script_files = request.FILES.getlist("script_files")

            for file in script_files:

                destination_path = os.path.join(
                    bot_folder,
                    file.name
                )

                os.makedirs(
                    os.path.dirname(destination_path),
                    exist_ok=True
                )

                with open(destination_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

        else:

            return JsonResponse(
                {
                    "status": "Error",
                    "description": "Invalid upload type"
                }
            )

        # ----------------------------
        # Save metadata in database
        # ----------------------------
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "bot_name": bot_name,
            "branch": branch,
            "status": status,
            "script_path": bot_folder
        }

        databaseBot = Database()

        response = databaseBot.Add_bot(payload)

        return JsonResponse(
            {
                "status": "Complete",
                "description": response
            }
        )

    except Exception as e:

        print("ERROR:", str(e))

        return JsonResponse(
            {
                "status": "Error",
                "description": str(e)
            }
        )
def runBot(request):
    if request.method == "POST":
        data = json.loads(request.body)

        bot = Bot()

        response = bot.run_bot(data)
        print(type(response))
        print(response)
        return JsonResponse(response)
def stopBot(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            bot = Bot()

            response = bot.stop_bot(data)

            return JsonResponse({
                "status": "Complete",
                "description": response
            })
                
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "desciption": str(e)
        })

def botRunDetails(request, botId):
    print("botId",botId)
    dataBase = Database()

    response = dataBase.view_runs(botId)
    return render(request,"botDetails.html", response)

def logDetails(request, runId):
    dataBase = Database()

    response  =dataBase.view_logs(runId)

    return render(request, "logDetails.html", response)
def DeleteBot(request):
    try:
        bot_name = request.POST["bot_name"]
        
        bot = Database()

        bot_data = bot.get_bot_by_name(bot_name)
        

        if bot_data.get("status") == "Error":
            return JsonResponse(bot_data)

        bot_id = bot_data["id"]
        source = script_path = bot_data["script_path"]
        

        # destination = os.path.join(
        #     settings.DELETED_BOT_STORAGE_PATH,
        #     os.path.basename(source)
        # )

        # shutil.move(source, destination)

        runs_data = bot.view_runs(bot_id)
        for run in runs_data["bots"]:
            run_id = run["id"]
            DeleteLogResponse = bot.delete_logs(run_id)
            print("Response fron delete Logs:", DeleteLogResponse)
            

        DeleteRunsResponse  = bot.delete_runs(bot_id)

        print("Response fron delete Logs:", DeleteLogResponse)

        DeleteBots = bot.delete_bots(bot_name)

        print("Response from delete Bots", DeleteBots)

        return JsonResponse({
            "status" : "Delete Complete",
            "description" : "Bot Deleted SUccessfully"
        })
    except Exception as e:
        return JsonResponse({
            "status" : "Delete Failed",
            "description" : str(e)
        })

