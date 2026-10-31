import os, signal, sys, time
def bye(signum, frame):
    print(f"[server] pid={os.getpid()} got SIGTERM, shutting down cleanly", flush=True)
    sys.exit(0)
signal.signal(signal.SIGTERM, bye)
print(f"[server] pid={os.getpid()} ppid={os.getppid()} started", flush=True)
while True:
    time.sleep(0.2)
