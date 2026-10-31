# Runs on this machine, no Docker needed: the same failures a container shows.
d=$(mktemp -d); cd "$d"
printf '#!/bin/sh\r\necho hello\r\n' > crlf.sh;  chmod +x crlf.sh
printf '#!/bin/sh\necho hello\n'     > noexec.sh   # no chmod +x
printf '#!/bin/sh\necho hello\n'     > ok.sh;     chmod +x ok.sh
echo "--- CRLF script:";      ./crlf.sh;  echo "exit=$?"
echo "--- missing x bit:";    ./noexec.sh; echo "exit=$?"
echo "--- not in PATH:";      nosuchcmd;  echo "exit=$?"
echo "--- fixed CRLF (tr -d '\\r'):"; tr -d '\r' < crlf.sh > fixed.sh; chmod +x fixed.sh; ./fixed.sh; echo "exit=$?"
echo "--- what file/od shows for the CRLF script:"; od -c crlf.sh | head -2
