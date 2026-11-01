# Q15: why 127.0.0.1 inside the container is the bug. Same idea on one machine: connect via the non-loopback address.
import socket, threading
def serve(bind):
    s = socket.socket(); s.bind((bind, 0)); s.listen(1); return s
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); u.connect(("10.255.255.255", 1))  # no packet sent; picks the outbound interface
non_loop = u.getsockname()[0]; u.close()
for bind in ("127.0.0.1", "0.0.0.0"):
    s = serve(bind); port = s.getsockname()[1]
    # docker-proxy / NAT delivers traffic to the container's eth0 address, not its loopback
    c = socket.socket(); c.settimeout(1)
    try: c.connect((non_loop, port)); r = "connected"
    except OSError as e: r = f"failed ({type(e).__name__})"
    print(f"server bound to {bind:9} -> client via {non_loop}: {r}")
    c.close(); s.close()
