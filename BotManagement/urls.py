from django.contrib import admin
from django.urls import include, path
from .views import home,botPage, addBot, NewBot, EditBotPage , UserPage, DeleteBotPage, ExportLogs
from .views import runBot, stopBot, botRunDetails, profilePage, logDetails, EditBot, ViewBotCode, ViewFile,DeleteBot
from .views import workflowPage,workflowBuilder,workflowHistory,workflowDashboard,workflowDetails,workflowLogs, workflowMonitor,workflowBuilder,DeletedWorkflowPage
from .views import LoginPage, LogoutPage
# print("Add bot calling")
urlpatterns = [
    path('', home),
    path('addBot', addBot),
    path('botPage',botPage ),
    path('api/NewBot', NewBot),
    path('api/runBot', runBot),
    path('api/stopBot', stopBot),
    path('BotDetails/<int:botId>/', botRunDetails),
    path('logDetails/<int:runId>/', logDetails),
    path('EditBot', EditBotPage),
    path('api/EditBot', EditBot),
    path('api/viewBot', ViewBotCode),
    path('api/viewFile', ViewFile),
    path('users', UserPage),
    path('api/DeleteBot', DeleteBot),
    path('DeleteBot', DeleteBotPage),
    path("api/exportLogs/<int:run_id>",ExportLogs),
    path('workflowPage', workflowPage),
    path('workflowBuilder', workflowBuilder),
    path('Deletedworkflows',DeletedWorkflowPage),
    path('workflowHistory/<int:workflow_id>/', workflowHistory),
    path("workflowLogs/<int:workflow_run_id>/",workflowLogs),
    path("login/",LoginPage),
    path("logout/",LogoutPage),
]
