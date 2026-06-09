# transaction_bot.py

from helpers.test_helper.email_helper import send_email
from helpers.test_helper.logger import log
from helpers.test_helper.utils.validator import validate_email

log("Bot Started")

receiver = "abc@gmail.com"

if validate_email(receiver):
    send_email(
        receiver,
        "Transaction Alert",
        "Rs. 1000 credited to your account."
    )
else:
    log("Invalid email address")

log("Bot Finished")