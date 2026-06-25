from .modules.workflow_database_module import WorkflowDatabaseModule
from ..workflow_engine.engine import WorkflowEngine
import os
import shutil
from django.conf import settings

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

        workflow_folder = os.path.join(

            settings.WORKFLOW_STORAGE_PATH,

            f"workflow_{workflow_name}"

        )

        os.makedirs(

            workflow_folder,

            exist_ok=True

        )

        nodes = workflow["drawflow"]["Home"]["data"]

        for node_id, node in nodes.items():

            node_folder = os.path.join(

                workflow_folder,

                f"node_{node_id}"

            )

            os.makedirs(

                node_folder,

                exist_ok=True

            )

            script_path = os.path.join(

                node_folder,

                "main.py"

            )

            node["data"]["script_path"] = script_path
            # print(node_id)
            # print(node["data"]["script_path"])

            code = node["data"].get(

                "script_content",

                ""

            )

            with open(

                script_path,

                "w"

            ) as f:

                f.write(

                    code

                )

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

            # Get workflow information
            workflow = self.database.get_workflow_by_id(

                workflow_id

            )

            workflow_name = workflow["workflow_name"]

            source_folder = os.path.join(

                settings.WORKFLOW_STORAGE_PATH,

                f"workflow_{workflow_name}"

            )

            destination_root = (

                settings.DELETED_WORKFLOW_PATH

            )

            os.makedirs(

                destination_root,

                exist_ok=True

            )

            destination_folder = os.path.join(

                destination_root,

                f"workflow_{workflow_name}"

            )

            # Move workflow folder
            if os.path.exists(

                source_folder

            ):

                shutil.move(

                    source_folder,

                    destination_folder

                )

            # Delete from database
            response = self.database.delete_workflow(

                workflow_id

            )

            return {

                "status": "deleted",

                "description": response

            }

        except Exception as e:
            # print("Deleted Workflow Error:", str(e))

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

    def get_workflow_code(
    self,
    workflow_name
):

        workflow_folder = os.path.join(
            settings.WORKFLOW_STORAGE_PATH,
            f"workflow_{workflow_name}"
        )

        files = []

        for dirname in sorted(os.listdir(workflow_folder)):

            node_folder = os.path.join(
                workflow_folder,
                dirname
            )

            if os.path.isdir(node_folder):

                # Add folder
                files.append(

                    {

                        "path": dirname,

                        "name": dirname,

                        "depth": 0,

                        "type": "folder"

                    }

                )

                # Add files inside folder
                for filename in sorted(os.listdir(node_folder)):

                    full_path = os.path.join(
                        node_folder,
                        filename
                    )

                    if os.path.isfile(full_path):

                        files.append(

                            {

                                "path": f"{dirname}/{filename}",

                                "name": filename,

                                "depth": 1,

                                "type": "file"

                            }

                        )

        selected_file = "node_1/main.py"

        code = ""

        default_file = os.path.join(

            workflow_folder,

            selected_file

        )

        if os.path.exists(default_file):

            with open(

                default_file,

                "r"

            ) as f:

                code = f.read()

        return {

            "files": files,

            "code": code,

            "selected_file": selected_file

        }