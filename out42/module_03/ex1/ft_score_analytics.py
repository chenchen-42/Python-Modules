import sys


def main() -> None:
    print("=== Player Score Analytics ===")

    scores: list[int] = []
    for argument in sys.argv[1:]:
        try:
            scores.append(int(argument))
        except ValueError:
            print(f"Invalid parameter: '{argument}'")

    if len(scores) == 0:
        print("No scores provided. "
              "Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return

    total: int = sum(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {total / len(scores)}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    main()
