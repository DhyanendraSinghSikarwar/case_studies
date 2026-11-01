"""Fake dependency: opens a TCP port after a delay."""
import socket, sys, time
time.sleep(float(sys.argv[2]))
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", int(sys.argv[1]))); s.listen()
time.sleep(30)
