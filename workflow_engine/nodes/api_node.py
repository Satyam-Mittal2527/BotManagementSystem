import requests


class APINode:

    def __init__(self, data):
        self.data = data

    def execute(self, context):

        try:

            response = requests.get(
                self.data["url"]
            )

            response.raise_for_status()

            context["api_response"] = response.json()

            print(
                "API Response:",
                context["api_response"]
            )

            return True

        except Exception as e:

            print(
                "API Error:",
                e
            )

            return False