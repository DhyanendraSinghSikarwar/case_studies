import base64
secret = "s3cr3t-token-123"
masked = lambda line: line.replace(secret, "***")      # what log masking does: exact-string match
for label, line in [("exact", f"token={secret}"),
                    ("base64", "token=" + base64.b64encode(secret.encode()).decode()),
                    ("split", "token=" + secret[:6] + " " + secret[6:])]:
    print(f"{label:7}-> {masked(line)}")
