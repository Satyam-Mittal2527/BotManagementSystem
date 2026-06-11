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

                            if edge["label"] == "True"

                        ),

                        None

                    )

                else:

                    next_edge = next(

                        (
                            edge

                            for edge in all_edges

                            if edge["label"] == "False"

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