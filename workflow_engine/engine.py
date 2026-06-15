from workflow_engine.registry import NODE_MAP
from modules.workflow_database_module import WorkflowDatabaseModule


class WorkflowEngine:

    def execute(self, workflow, workflow_id):

        context = {}

        database = WorkflowDatabaseModule()

        workflow_run_id = database.insert_workflow_run(
            workflow_id
        )

        current_node = workflow["nodes"][0]["id"]

        while current_node:
            print("Current node:", current_node)
            print("Workflow nodes:")

            for n in workflow["nodes"]:
                print(n)

            node = next(
                (
                    n
                    for n in workflow["nodes"]
                    if n["id"] == current_node
                ),
                None
            )

            if node is None:

                database.update_workflow_run(
                    workflow_run_id,
                    "FAILED"
                )

                raise Exception(
                    f"Node {current_node} not found"
                )

            # Execute node
            print(node["type"])
            print(NODE_MAP)
            node_class = NODE_MAP[node["type"]]

            node_obj = node_class(
                node["data"]
            )

            try:

                result = node_obj.execute(

                    context,

                    database,

                    workflow_run_id

                )

                database.insert_node_run(

                    workflow_run_id,

                    node["id"],

                    node["type"],

                    "SUCCESS",

                    "Executed Successfully"

                )

                print(result)

            except Exception as e:

                database.insert_node_run(

                    workflow_run_id,

                    node["id"],

                    node["type"],

                    "FAILED",

                    str(e)

                )

                database.update_workflow_run(

                    workflow_run_id,

                    "FAILED"

                )

                raise e

            # Find all outgoing edges
            all_edges = [

                edge

                for edge in workflow["edges"]

                if edge["source"] == current_node

            ]

            # Condition node
            if node["type"] == "condition":

                if result:

                    next_edge = next(

                        (
                            edge

                            for edge in all_edges

                            if edge.get("label") == "True"

                        ),

                        None

                    )

                else:

                    next_edge = next(

                        (
                            edge

                            for edge in all_edges

                            if edge.get("label") == "False"

                        ),

                        None

                    )

            # Other nodes
            else:

                next_edge = all_edges[0] if all_edges else None

            # Move to next node
            if next_edge:

                current_node = next_edge["target"]

            else:

                current_node = None

        database.update_workflow_run(

            workflow_run_id,

            "COMPLETED"

        )