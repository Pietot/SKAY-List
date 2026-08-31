import subprocess
import sys

ID = ""

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "add_level.py",
        "--type",
        "extreme",
        "--id",
        ID,
    ]
    cmd.extend(sys.argv[1:])
    subprocess.run(cmd, check=False)
