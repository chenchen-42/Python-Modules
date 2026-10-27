import sys


def parse_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for argument in arguments:
        parts: list[str] = argument.split(":")
        if len(parts) != 2 or parts[0] == "":
            print(f"Error - invalid parameter '{argument}'")
            continue
        name: str = parts[0]
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            quantity: int = int(parts[1])
        except ValueError as error:
            print(f"Quantity error for '{name}': {error}")
            continue
        if quantity < 0:
            print(f"Quantity error for '{name}': negative quantity")
            continue
        inventory.update({name: quantity})
    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")

    items: list[str] = list(inventory.keys())
    print(f"Item list: {items}")

    total: int = sum(inventory.values())
    print(f"Total quantity of the {len(items)} items: {total}")

    if len(items) == 0 or total == 0:
        print("Nothing to analyse in an empty inventory.")
    else:
        for item in items:
            percent: float = round(inventory[item] / total * 100, 1)
            print(f"Item {item} represents {percent}%")

        most: str = items[0]
        least: str = items[0]
        for item in items:
            if inventory[item] > inventory[most]:
                most = item
            if inventory[item] < inventory[least]:
                least = item
        print(f"Item most abundant: {most} with quantity {inventory[most]}")
        print(f"Item least abundant: {least} with quantity "
              f"{inventory[least]}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
