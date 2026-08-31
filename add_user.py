import argparse
import json
import subprocess
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
EXTREMES_DIR = DATA_DIR / "extremes"
EXTREME_LIST_PATH = DATA_DIR / "_extreme_list.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")


def get_record_user(profile):
    return profile.get("global_name") or profile.get("username") or "Unknown"


def extract_record(profile_record) -> tuple[str, str, str]:
    level_info = profile_record["level"]
    level_id = level_info["level_id"]
    level_name = level_info["name"]
    link = profile_record["video_url"]

    return str(level_id), str(level_name), str(link)


def add_user_records(username: str):
    url = f"https://api.aredl.net/v2/api/aredl/profile/{username}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    profile = response.json()

    user_name = get_record_user(profile)
    records = profile["records"]

    if not isinstance(records, list):
        raise ValueError(
            f"The profile response for '{username}' does not contain a valid records list."
        )

    for profile_record in records:
        level_id, level_name, link = extract_record(profile_record)
        cmd = [
            "python",
            "add_extreme.py",
            "--type",
            "extreme",
            "--id",
            level_id,
        ]
        subprocess.run(cmd, check=False)

        cmd = [
            "python",
            "add_record_fast.py",
            "--type",
            "extreme",
            "--name",
            level_name,
            "--user",
            user_name,
            "--link",
            link,
        ]
        subprocess.run(cmd, check=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add all extreme demon completions for a user based on their AREDL username."
    )
    parser.add_argument("--username", required=True, help="AREDL username to fetch.")
    args = parser.parse_args()

    try:
        add_user_records(args.username)
    except Exception as e:
        print(e)
        raise SystemExit(1)

    print(f"Updated extreme level files for {args.username}.")


if __name__ == "__main__":
    main()
