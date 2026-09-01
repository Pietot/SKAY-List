import re
import subprocess
import sys

NAME = ""
TYPE = ""
USER = ""
LINK = ""

def strip_url_keys(url: str) -> str:
    return re.sub(r"([?&])(?:list|index|pp|si)=[^&]+", "", url)

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
        strip_url_keys(LINK),
    ]
    cmd.extend(sys.argv[1:])
    subprocess.run(cmd, check=False)
