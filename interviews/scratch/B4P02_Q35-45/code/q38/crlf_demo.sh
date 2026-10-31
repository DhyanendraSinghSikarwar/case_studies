#!/usr/bin/env bash
# Q38 pitfalls: CRLF line endings and a missing executable bit
d=$(mktemp -d); cd "$d"
printf '#!/usr/bin/env bash\r\necho hello\r\n' > crlf.sh; chmod +x crlf.sh
echo "== CRLF script"; ./crlf.sh; echo "exit=$?"
printf '#!/usr/bin/env bash\necho hello\n' > noexec.sh
echo "== no executable bit"; ./noexec.sh; echo "exit=$?"
echo "== fix: strip CR (sed -i 's/\r$//') and chmod +x"
sed -i 's/\r$//' crlf.sh; ./crlf.sh; echo "exit=$?"
rm -rf "$d"
