from workflow.workflow_service import WorkflowService
import json
import os
from django.conf import settings
from django.http import JsonResponse
workflowService = WorkflowService()

def run_workflow(request, workflow_id):
    print("WorkflowID:", workflow_id)
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

        return JsonResponse(

            {

                "status": "error",

                "message": str(e)

            }

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
def get_history(request, workflow_id):

    history = workflowService.get_history(
        workflow_id
    )
    
    return JsonResponse(
        history
    )

def get_all_workflows(request):

    workflows = workflowService.get_all_workflows()

    return JsonResponse(

        workflows,

        safe=False

    )
def get_dashboard(request):

    dashboard = workflowService.get_dashboard()

    return JsonResponse(
        dashboard
    )

def UploadNodeScript(request):

    try:

        node_id = request.POST["node_id"]

        file = request.FILES["script"]

        workflow_name = request.POST["workflow_name"]

        node_folder = os.path.join(

            settings.WORKFLOW_STORAGE_PATH,

            f"workflow_{workflow_name}",

            f"node_{node_id}"

        )


        os.makedirs(

            node_folder,

            exist_ok=True

        )


        destination_path = os.path.join(

            node_folder,

            "main.py"

        )


        with open(

            destination_path,

            "wb+"

        ) as destination:

            for chunk in file.chunks():

                destination.write(

                    chunk

                )
        

        return JsonResponse(

            {

                "status":"success",

                "script_path":

                destination_path

            }

        )

    except Exception as e:

        return JsonResponse(

            {

                "status":"error",

                "message":

                str(e)

            }

        )

def getWorkflowLogs(

    request,

    workflow_run_id

):
    logs = workflowService.getWorkflowLogs(workflow_run_id)
    

    return JsonResponse(

        {

            "logs": logs

        }

    )