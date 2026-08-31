import subprocess
import sys

NAME = ""
TYPE = ""
USER = ""
LINK = ""
HZ = ""

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "add_record.py",
        "--type",
        TYPE,
        "--name",
        NAME,
        "--user",
        USER,
        "--link",
        LINK,
    ]
    cmd.extend(sys.argv[1:])
    subprocess.run(cmd, check=False)
