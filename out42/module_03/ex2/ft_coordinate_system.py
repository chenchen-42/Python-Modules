import math


def get_player_pos() -> tuple[float, float, float]:
    prompt: str = "Enter new coordinates as floats in format 'x,y,z': "
    while True:
        try:
            raw: str = input(prompt)
        except EOFError:
            print("\nNo more input, using (0.0, 0.0, 0.0)")
            return (0.0, 0.0, 0.0)

        parts: list[str] = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue

        values: list[float] = []
        try:
            for part in parts:
                values.append(float(part))
        except ValueError as error:
            print(f"Error on parameter '{part.strip()}': {error}")
            continue

        return (values[0], values[1], values[2])


def distance(a: tuple[float, float, float],
             b: tuple[float, float, float]) -> float:
    x1, y1, z1 = a
    x2, y2, z2 = b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def main() -> None:
    print("=== Game Coordinate System ===")

    print("\nGet a first set of coordinates")
    first: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {first}")
    x, y, z = first
    print(f"It includes: X={x}, Y={y}, Z={z}")
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    print(f"Distance to center: {round(distance(first, center), 4)}")

    print("\nGet a second set of coordinates")
    second: tuple[float, float, float] = get_player_pos()
    print("Distance between the 2 sets of coordinates: "
          f"{round(distance(first, second), 4)}")


if __name__ == "__main__":
    main()
