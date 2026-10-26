"""Q36: is the docker socket here, who owns it, and could I use it? Run: python3 -I sock_check.py"""
import grp, os, stat

SOCK = "/var/run/docker.sock"
try:
    st = os.stat(SOCK)
except FileNotFoundError:
    print(f"{SOCK}: not found -> no local dockerd; the docker CLI has nothing to talk to")
else:
    print("is socket:", stat.S_ISSOCK(st.st_mode), "| mode:", oct(st.st_mode & 0o777),
          "| group:", grp.getgrgid(st.st_gid).gr_name)
    print("my uid:", os.getuid(), "| my groups:", [grp.getgrgid(g).gr_name for g in os.getgroups()])
print("DOCKER_HOST env:", os.environ.get("DOCKER_HOST", "(not set)"))
print("rule of thumb: anyone who can write to that socket can start a container with -v /:/host = root on the host")
