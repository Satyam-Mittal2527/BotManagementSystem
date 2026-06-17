from .registry import NODE_MAP
from ..workflow.modules.workflow_database_module import WorkflowDatabaseModule


class WorkflowEngine:

    def execute(
        self,
        workflow,
        workflow_id
    ):

        print(
            "==============Executing the code===================="
        )

        context = {}

        database = WorkflowDatabaseModule()

        workflow_run_id = database.insert_workflow_run(
            workflow_id
        )

        # -------------------
        # Find Start Node
        # -------------------
        start_node = next(

            (

                node

                for node in workflow["nodes"]

                if node["type"] == "start"

            ),

            None

        )

        if start_node is None:

            database.update_workflow_run(

                workflow_run_id,

                "FAILED"

            )

            raise Exception(

                "No Start Node found in workflow"

            )

        current_node = start_node["id"]

        while current_node:

            print(
                "Current node:",
                current_node
            )

            print(
                "Context =",
                context
            )

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

            print(
                "Executing node type:",
                node["type"]
            )

            node_class = NODE_MAP[
                node["type"]
            ]
            print("NODE DATA =", node["data"])
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

                print(
                    "Result =",
                    result
                )

                print(
                    "Updated Context =",
                    context
                )

            except Exception as e:

                print(

                    "ERROR OCCURRED:",

                    str(e)

                )

                database.insert_log(

                    workflow_run_id,

                    node["id"],

                    "ERROR",

                    str(e)

                )

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

                raise

            # -------------------
            # Find outgoing edges
            # -------------------
            all_edges = [

                edge

                for edge in workflow["edges"]

                if edge["source"] == current_node

            ]

            # -------------------
            # Condition / Decision / Loop
            # -------------------
            if node["type"] in [

                "condition",

                "decision",

                "loop"

            ]:

                if result:

                    next_edge = next(

                        (

                            edge

                            for edge in all_edges

                            if edge.get(
                                "label"
                            ) == "True"

                        ),

                        None

                    )

                else:

                    next_edge = next(

                        (

                            edge

                            for edge in all_edges

                            if edge.get(
                                "label"
                            ) == "False"

                        ),

                        None

                    )

            # -------------------
            # Normal nodes
            # -------------------
            else:

                next_edge = (

                    all_edges[0]

                    if all_edges

                    else None

                )

            # -------------------
            # Move to next node
            # -------------------
            if next_edge:

                current_node = next_edge[
                    "target"
                ]

            else:

                current_node = None

        database.update_workflow_run(

            workflow_run_id,

            "COMPLETED"

        )

        return context