from django.urls import path, include
from . import views
urlpatterns = [

    path("run/<int:workflow_id>/",views.run_workflow),
    path("get/<int:workflow_id>/",views.get_workflow),
    path("save/",views.save_workflow),
    path("history/<int:workflow_id>/",views.get_history),
    path("delete/<int:workflow_id>/",views.delete_workflow),
    path("list/",views.get_all_workflows),
    path("dashboard/",views.get_dashboard),
    path("logs/<int:workflow_run_id>/", views.getWorkflowLogs),
    path("view/<str:workflow_name>/",views.ViewWorkflow),
    path("open_file/",views.open_file),
    path("edit_file/",views.edit_file)
]