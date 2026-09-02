import json
from pathlib import Path
import time

import requests

ROOT = Path(__file__).resolve().parent
EXTREME_LIST_PATH = ROOT / "data" / "_extreme_list.json"
EXTREMES_DIR = ROOT / "data" / "extremes"
API_URL = "https://api.aredl.net/v2/api/aredl/levels/{level_id}"


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_extreme_names() -> list[str]:
    if not EXTREME_LIST_PATH.exists():
        raise FileNotFoundError(f"Missing file: {EXTREME_LIST_PATH}")

    names = read_json(EXTREME_LIST_PATH)
    if not isinstance(names, list):
        raise ValueError(f"Expected a list in {EXTREME_LIST_PATH}")

    return [str(name) for name in names]


def refresh_level_points(level_name: str) -> int:
    level_path = EXTREMES_DIR / f"{level_name}.json"
    if not level_path.exists():
        raise FileNotFoundError(f"Missing extreme file: {level_path}")

    level_data = read_json(level_path)
    level_id = level_data.get("id")
    if level_id is None:
        raise ValueError(f"No id found in {level_path}")

    response = requests.get(API_URL.format(level_id=level_id), timeout=20)
    response.raise_for_status()
    payload = response.json()

    points = int(payload.get("points", 0))
    level_data["aredl_points"] = points
    write_json(level_path, level_data)
    time.sleep(0.5)
    return points


def sort_extremes_by_points() -> list[str]:
    ordered = []
    for level_name in load_extreme_names():
        level_path = EXTREMES_DIR / f"{level_name}.json"
        if not level_path.exists():
            ordered.append((0, level_name))
            continue

        data = read_json(level_path)
        ordered.append((int(data.get("aredl_points", 0)), level_name))

    sorted_names = [name for _, name in sorted(ordered, key=lambda item: item[0], reverse=True)]
    write_json(EXTREME_LIST_PATH, sorted_names)
    return sorted_names


def main() -> None:
    names = load_extreme_names()
    updated = 0

    for level_name in names:
        try:
            refresh_level_points(level_name)
            updated += 1
            print(f"Updated {level_name}")
        except Exception as exc:
            print(f"Failed to update {level_name}: {exc}")

    sort_extremes_by_points()
    print(f"Completed: updated {updated} extreme demon files")


if __name__ == "__main__":
    main()
