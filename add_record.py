import argparse
import json
from pathlib import Path

from models import Record

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def resolve_level_file(level_type: str, level_name: str) -> Path:
    level_dir = DATA_DIR / ("extremes" if level_type == "extreme" else "challenges")
    candidate = level_dir / f"{level_name}.json"
    if candidate.exists():
        return candidate

    list_file = DATA_DIR / (
        "_extreme_list.json" if level_type == "extreme" else "_challenge_list.json"
    )
    if list_file.exists():
        names = load_json(list_file)
        for item_name in names:
            file_path = level_dir / f"{item_name}.json"
            if file_path.exists() and item_name.lower() == level_name.lower():
                return file_path

    raise FileNotFoundError(
        f"Could not find a {level_type} level named '{level_name}' in {level_dir}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a record to an extreme or challenge level.")
    parser.add_argument(
        "--type", required=True, choices=["extreme", "challenge"], help="Type of the level."
    )
    parser.add_argument("--name", required=True, help="Name of the level in the JSON file.")
    parser.add_argument("--user", required=True, help="Username who got the record.")
    parser.add_argument("--link", required=True, help="Video link of the record.")
    parser.add_argument("--hz", type=int, default=60, help="Refresh rate in Hz.")
    args = parser.parse_args()

    try:
        level_path = resolve_level_file(args.type, args.name)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)

    data = load_json(level_path)
    if "records" not in data or data["records"] is None:
        data["records"] = []

    record = Record(user=args.user, link=args.link, hz=args.hz)
    data["records"].append(record.model_dump())

    save_json(level_path, data)

    print(f"Record added to {args.type} level '{args.name}' in {level_path.name}")


if __name__ == "__main__":
    main()
