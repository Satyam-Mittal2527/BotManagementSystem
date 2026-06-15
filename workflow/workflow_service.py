from modules.workflow_database_module import WorkflowDatabaseModule
from workflow_engine.engine import WorkflowEngine


class WorkflowService:

    def __init__(self):

        self.database = WorkflowDatabaseModule()

        self.engine = WorkflowEngine()


    def save_workflow(

        self,

        workflow_name,

        description,

        workflow

    ):

        workflow_id = self.database.save_workflow(

            workflow_name,

            description,

            workflow

        )

        return workflow_id


    def run_workflow(

        self,

        workflow_id

    ):
        print("WorkflowID_fromservice:", workflow_id)
        workflow = self.database.get_workflow(

            workflow_id

        )

        self.engine.execute(

            workflow,

            workflow_id

        )

        return True


    def get_workflow(

        self,

        workflow_id

    ):

        return self.database.get_workflow(

            workflow_id

        )


    def delete_workflow(

        self,

        workflow_id

    ):

        try:
            response = self.database.delete_workflow(workflow_id)

            return {
                "status": "deleted",
                "description": response
            }
        except Exception as e:
            return {
                "status": "error",
                "description": str(e)
            }

    def get_history(
    self,
    workflow_id
):

        workflow_runs = self.database.get_workflow_runs(
            workflow_id
        )

        node_runs = self.database.get_node_runs(
            workflow_id
        )

        return {

            "workflow_runs": workflow_runs,

            "node_runs": node_runs

        }
    def get_all_workflows(self):

        return self.database.get_all_workflows()

    def get_dashboard(self):

        return self.database.get_dashboard()
    def getWorkflowLogs(self,workflow_run_id):

        return self.database.get_logs(

            workflow_run_id
        )