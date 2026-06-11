class LoopNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        variable_name = self.data["variable"]

        items = context[variable_name]

        context["loop_items"] = items

        return True