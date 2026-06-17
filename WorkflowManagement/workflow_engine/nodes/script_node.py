import io
from contextlib import redirect_stdout


class ScriptNode:

    def __init__(self, data):

        self.data = data

    def execute(

        self,

        context,

        database,

        workflow_run_id

    ):

        script_path = self.data["script_path"]

        node_id = self.data["node_name"]

        database.insert_log(

            workflow_run_id,

            node_id,

            "INFO",

            f"Starting {node_id}"

        )

        namespace = context.copy()

        with open(

            script_path,

            "r",

            encoding="utf-8"

        ) as file:

            code = file.read()

        output_buffer = io.StringIO()

        try:

            with redirect_stdout(

                output_buffer

            ):

                exec(

                    code,

                    namespace

                )

        except Exception as e:

            database.insert_log(

                workflow_run_id,

                node_id,

                "ERROR",

                str(e)

            )

            raise

        output = output_buffer.getvalue()

        for line in output.splitlines():

            print(line)

            database.insert_log(

                workflow_run_id,

                node_id,

                "INFO",

                line

            )

        namespace.pop(

            "__builtins__",

            None

        )

        context.update(

            namespace

        )

        database.insert_log(

            workflow_run_id,

            node_id,

            "INFO",

            "Finished execution"

        )

        return None