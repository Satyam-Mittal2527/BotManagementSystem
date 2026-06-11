from workflow.workflow_service import WorkflowService
import json
from django.http import JsonResponse
workflowService = WorkflowService()

def run_workflow(request, workflow_id):

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