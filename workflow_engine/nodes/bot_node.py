from bot.bank_bot import Bot


class BotNode:

    def __init__(self, data):

        self.data = data

    def execute(self, context):

        bot = Bot()

        bot.run_bot(

            {
                "botId": self.data["botId"]
            }

        )

        return True