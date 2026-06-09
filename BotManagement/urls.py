from django.contrib import admin
from django.urls import include, path
from .views import home, botPage, addBot, NewBot, EditBotPage
from .views import runBot, stopBot, botRunDetails, profilePage, logDetails, EditBot, ViewBotCode, ViewFile
print("Add bot calling")
urlpatterns = [
    path('', home),
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
    path('api/viewFile', ViewFile)
]
