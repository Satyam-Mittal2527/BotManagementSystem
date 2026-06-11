class LogNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        print(
            "LOG:",
            self.data["message"]
        )

        return True