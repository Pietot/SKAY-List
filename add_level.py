import argparse
import json
import sys

import requests as r

from models import Challenge, ExtremeDemon


def sort_extreme_list_by_aredl_points(list_path: str = "data/_extreme_list.json") -> list[str]:
    try:
        with open(list_path, "r", encoding="utf-8") as f:
            item_names = json.load(f)
    except FileNotFoundError:
        return []

    ranked_items = []
    for item_name in item_names:
        file_path = f"data/extremes/{item_name}.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                item = json.load(f)
            ranked_items.append((item.get("aredl_points", 0), item_name))
        except FileNotFoundError:
            ranked_items.append((0, item_name))

    sorted_items = [
        name for _, name in sorted(ranked_items, key=lambda pair: pair[0], reverse=True)
    ]

    with open(list_path, "w", encoding="utf-8") as f:
        json.dump(sorted_items, f, indent=4)

    return sorted_items


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add a new extreme demon or challenge to the JSON file."
    )
    parser.add_argument(
        "--type",
        type=str,
        help="The type of the item to add (extreme or challenge).",
        choices=["extreme", "challenge"],
        required=True,
    )
    parser.add_argument("--id", type=str, help="The ID of the item to add.", required=True)
    parser.add_argument("--name", type=str, help="The name of the challenge to add.")
    parser.add_argument("--author", type=str, help="The author of the challenge to add.")
    parser.add_argument(
        "--creators", type=str, nargs="+", help="The creators of the challenge to add."
    )
    parser.add_argument("--verifier", type=str, help="The verifier of the challenge to add.")
    parser.add_argument(
        "--verification", type=str, help="The verification link of the challenge to add."
    )
    args = parser.parse_args()

    if args.type == "extreme":
        level_detail = f"https://api.aredl.net/v2/api/aredl/levels/{args.id}"
        creators_details = f"https://api.aredl.net/v2/api/aredl/levels/{args.id}/creators"

        response = r.get(level_detail, timeout=10)
        if response.status_code == 200:
            level_data = response.json()
        else:
            print(
                f"Error: Unable to fetch data for ID {args.id}. Status code: {response.status_code}"
            )
            sys.exit(1)

        creators_response = r.get(creators_details, timeout=10)
        if creators_response.status_code == 200:
            creators_data = creators_response.json()
        else:
            print(
                f"Error: Unable to fetch creators data for ID {args.id}. Status code: {creators_response.status_code}"
            )
            sys.exit(1)

        creators_list = [creator["global_name"] for creator in creators_data]

        new_item = ExtremeDemon(
            id=args.id,
            name=level_data["name"],
            author=level_data["publisher"]["global_name"],
            creators=creators_list,
            verifier=level_data["verifications"][-1]["submitted_by"]["global_name"],
            aredl_points=level_data["points"],
        )
        # check if the name is already in the JSON file
        with open("data/_extreme_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if any(item == new_item.name for item in data):
                print(f"Error: An extreme demon with the name '{new_item.name}' already exists.")
                sys.exit(1)
            data.append(new_item.name)

        with open("data/_extreme_list.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        with open(f"data/extremes/{new_item.name}.json", "w", encoding="utf-8") as f:
            json.dump(new_item.model_dump(), f, indent=4)

        sort_extreme_list_by_aredl_points()

    elif args.type == "challenge":
        new_item = Challenge(
            id=args.id,
            name=args.name,
            author=args.author,
            creators=args.creators,
            verifier=args.verifier,
        )

        # check if the name is already in the JSON file
        with open("data/_challenge_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if any(item == new_item.name for item in data):
                print(f"Error: A challenge with the name '{new_item.name}' already exists.")
                sys.exit(1)
            data.append(new_item.name)

        with open("data/_challenge_list.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        with open(f"data/challenges/{new_item.name}.json", "w", encoding="utf-8") as f:
            json.dump(new_item.model_dump(), f, indent=4)
