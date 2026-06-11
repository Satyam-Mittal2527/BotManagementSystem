class VariableNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        context[
            self.data["name"]
        ] = self.data["value"]

        return context