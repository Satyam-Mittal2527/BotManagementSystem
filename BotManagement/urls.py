from django.contrib import admin
from django.urls import include, path
from .views import home, botPage, addBot, NewBot, EditBotPage , UserPage, DeleteBotPage, ExportLogs
from .views import runBot, stopBot, botRunDetails, profilePage, logDetails, EditBot, ViewBotCode, ViewFile,DeleteBot

print("Add bot calling")
urlpatterns = [
    path('', botPage),
    path('addBot', addBot),
    path('botPage',botPage ),
    path('api/NewBot', NewBot),
    path('api/runBot', runBot),
    path('api/stopBot', stopBot),
    path('BotDetails/<int:botId>/', botRunDetails),
    path('logDetails/<int:runId>/', logDetails),
    path('profile', profilePage),
    path('EditBot', EditBotPage),
    path('api/EditBot', EditBot),
    path('api/viewBot', ViewBotCode),
    path('api/viewFile', ViewFile),
    path('users', UserPage),
    path('api/DeleteBot', DeleteBot),
    path('DeleteBot', DeleteBotPage),
    path("api/exportLogs/<int:run_id>",ExportLogs)
]
