from workflow_engine.registry import NODE_MAP


class WorkflowEngine:

    def execute(self, workflow):

        context = {}

        current_node = "1"

        while current_node:

            # Find node
            node = next(
                n for n in workflow["nodes"]
                if n["id"] == current_node
            )

            # Execute node
            node_class = NODE_MAP[node["type"]]

            node_obj = node_class(
                node["data"]
            )

            result = node_obj.execute(
                context
            )

            print(result)

            # Find next edge
            next_edge = next(
                (
                    edge
                    for edge in workflow["edges"]
                    if edge["source"] == current_node
                ),
                None
            )

            # Move to next node
            if next_edge:

                current_node = next_edge["target"]

            else:

                current_node = None