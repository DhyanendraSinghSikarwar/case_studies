import time, os
print(f"[pid {os.getpid()}] server ready (no SIGTERM handler)", flush=True)
while True: time.sleep(0.1)
