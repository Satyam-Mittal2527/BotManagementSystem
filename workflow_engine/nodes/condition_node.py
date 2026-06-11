class ConditionNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        code = self.data["code"]

        result = eval(
            code,
            {},
            context
        )

        return result