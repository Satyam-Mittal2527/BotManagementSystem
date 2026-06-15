import subprocess


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

            f"Starting {script_path}"

        )

        process = subprocess.Popen(

            ["python", script_path],

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            bufsize=1

        )

        output = []

        for line in process.stdout:

            line = line.strip()

            print(line)

            output.append(line)

            database.insert_log(

                workflow_run_id,

                node_id,

                "INFO",

                line

            )

        process.wait()

        database.insert_log(

            workflow_run_id,

            node_id,

            "INFO",

            "Finished execution"

        )

        return "\n".join(output)