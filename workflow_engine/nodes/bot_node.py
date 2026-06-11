class BotNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        print(
            "Running Bot",
            self.data["botId"]
        )

        return True