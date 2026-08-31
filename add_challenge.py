import subprocess
import sys

ID = ""
NAME = ""
AUTHOR = ""
CREATORS = [""]
VERIFIER = ""
VERIFICATION = ""

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
    ]
    cmd.extend(sys.argv[1:])
    subprocess.run(cmd, check=False)
