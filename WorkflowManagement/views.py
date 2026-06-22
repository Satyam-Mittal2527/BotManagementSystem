from .workflow.workflow_service import WorkflowService
import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required

workflowService = WorkflowService()


@permission_required(
    "accounts.run_workflow",
    raise_exception=True
)
def run_workflow(request, workflow_id):
    # print("WorkflowID:", workflow_id)
    try:

        workflowService.run_workflow(
            workflow_id
        )

        return JsonResponse(
            {
                "status": "success"
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            }
        )
@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def get_workflow(request, workflow_id):

    try:

        workflow = workflowService.get_workflow(
            workflow_id
        )

        return JsonResponse(
            workflow
        )

    except Exception as e:

        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            }
        )


@permission_required(
    "accounts.edit_workflow",
    raise_exception=True
)
def save_workflow(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "status": "error"
            }
        )

    try:

        body = json.loads(
            request.body
        )
        # print(body)
        workflow_id = workflowService.save_workflow(

            body["workflow_name"],

            body["description"],

            body["workflow"]

        )

        return JsonResponse(

            {

                "status": "success",

                "workflow_id": workflow_id

            }

        )

    except Exception as e:
        # print(str(e))
        return JsonResponse(

            {

                "status": "error",

                "message": str(e)

            }

        )
@permission_required(
    "accounts.delete_workflow",
    raise_exception=True
)
def delete_workflow(request, workflow_id):

    workflowService.delete_workflow(
        workflow_id
    )

    return JsonResponse(
        {
            "status": "success"
        }
    )

@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def get_history(request, workflow_id):

    history = workflowService.get_history(
        workflow_id
    )
    
    return JsonResponse(
        history
    )


@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def get_all_workflows(request):

    workflows = workflowService.get_all_workflows()

    return JsonResponse(

        workflows,

        safe=False

    )

@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def get_dashboard(request):

    dashboard = workflowService.get_dashboard()

    return JsonResponse(
        dashboard
    )

# def UploadNodeScript(request):

#     try:
#         print("==== UploadNodeScript called ====")\

#         node_id = request.POST["node_id"]

#         workflow_name = request.POST["workflow_name"]

#         node_folder = os.path.join(

#             settings.WORKFLOW_STORAGE_PATH,

#             f"workflow_{workflow_name}",

#             f"node_{node_id}"

#         )
#         print(node_folder)
#         os.makedirs(

#             node_folder,

#             exist_ok=True

#         )

#         print("Folder created")
#         destination_path = os.path.join(

#             node_folder,

#             "main.py"

#         )

#         # Case 1 : User uploaded a file
#         if "script" in request.FILES:

#             file = request.FILES["script"]

#             with open(

#                 destination_path,

#                 "wb+"

#             ) as destination:

#                 for chunk in file.chunks():

#                     destination.write(

#                         chunk

#                     )

#         # Case 2 : Monaco editor code
#         else:

#             script_content = request.POST["script_content"]

#             with open(

#                 destination_path,

#                 "w",

#                 encoding="utf-8"

#             ) as destination:

#                 destination.write(

#                     script_content

#                 )

#         return JsonResponse(

#             {

#                 "status": "success",

#                 "script_path": destination_path

#             }

#         )

#     except Exception as e:

#         return JsonResponse(

#             {

#                 "status": "error",

#                 "message": str(e)

#             }

#         )

@permission_required(
    "accounts.view_logs",
    raise_exception=True
)
def getWorkflowLogs(

    request,

    workflow_run_id

):  
    # print("Reached views")
    # print(workflow_run_id)
    logs = workflowService.getWorkflowLogs(workflow_run_id)
    

    return JsonResponse(

        {

            "logs": logs

        }

    )


@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def ViewWorkflow(

    request,

    workflow_name

):

    workflow_data =  workflowService.get_workflow_code(

        workflow_name

    )
    workflow_data.update(

        {

            "bot_name": workflow_name

        }

    )   
    return render(

        request,

        "ViewWorkflow.html",

        workflow_data

    )

@permission_required(
    "accounts.view_workflow",
    raise_exception=True
)
def open_file(request):

    try:

        body = json.loads(
            request.body
        )

        # print(body)

        workflow_folder = os.path.join(

            settings.WORKFLOW_STORAGE_PATH,

            f"workflow_{body['workflow_name']}"

        )

        file_path = os.path.join(

            workflow_folder,

            body["file_path"]

        )

        # print(file_path)

        with open(

            file_path,

            "r"

        ) as f:

            code = f.read()

        return JsonResponse(

            {

                "code": code

            }

        )

    except Exception as e:

        # print("ERROR:", str(e))

        return JsonResponse(

            {

                "status": "error",

                "message": str(e)

            }

        )

@permission_required(
    "accounts.edit_workflow",
    raise_exception=True
)
def edit_file(request):

    body = json.loads(
        request.body
    )

    workflow_folder = os.path.join(

        settings.WORKFLOW_STORAGE_PATH,

        f"workflow_{body['workflow_name']}"

    )

    file_path = os.path.join(

        workflow_folder,

        body["file_path"]

    )

    with open(

        file_path,

        "w"

    ) as f:

        f.write(

            body["code"]

        )

    return JsonResponse(

        {

            "status": "success",

            "message": "File updated successfully"

        }

    )
