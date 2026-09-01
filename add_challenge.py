import subprocess
import sys

ID = ""
NAME = ""
AUTHOR = ""
CREATORS = [""]
VERIFIER = ""
VERIFICATION = ""
ATTEMPTS = ""
ENJOYMENT = ""

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "add_level.py",
        "--type",
        "challenge",
        "--id",
        ID,
        "--name",
        NAME,
        "--author",
        AUTHOR,
        "--creators",
        *CREATORS,
        "--verifier",
        VERIFIER,
        "--verification",
        VERIFICATION,
        "--attempts",
        ATTEMPTS,
        "--enjoyment",
        ENJOYMENT,
    ]
    cmd.extend(sys.argv[1:])
    subprocess.run(cmd, check=False)
