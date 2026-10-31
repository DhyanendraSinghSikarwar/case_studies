import signal, sys, time, os
def on_term(signum, frame):
    print(f"[pid {os.getpid()}] got SIGTERM, finishing in-flight work, saving checkpoint", flush=True)
    sys.exit(0)
signal.signal(signal.SIGTERM, on_term)
print(f"[pid {os.getpid()}] server ready", flush=True)
while True: time.sleep(0.1)
