class ConditionNode:

    def __init__(self, data):

        self.data = data

    def execute(

        self,

        context,

        database,

        workflow_run_id

    ):

        namespace = context.copy()

        with open(

            self.data["script_path"]

        ) as f:

            code = f.read()

        exec(

            code,

            namespace

        )

        result = namespace["result"]

        return bool(result)