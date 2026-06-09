import time
import json

from helper import send_email

print("Email Bot Started", flush=True)

with open("config.json") as f:
    config = json.load(f)

for i in range(5):
    send_email()

    print(
        f"Email sent to {config['email']} ({i+1}/5)",
        flush=True
    )

    time.sleep(config["interval"])

print("Email Bot Finished", flush=True)