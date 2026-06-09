import time

print("Bot started", flush=True)

i = 0

while True:
    i += 1

    print(f"Working... {i}", flush=True)

    time.sleep(5)

    if i == 5:
        break

print("Bot completed", flush=True)