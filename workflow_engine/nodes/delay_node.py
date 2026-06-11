import time


class DelayNode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        seconds = self.data["seconds"]

        print(f"Sleeping {seconds} sec")

        time.sleep(seconds)

        return True