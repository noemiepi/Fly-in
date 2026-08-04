from src.parsing.map_parse import MapParser


end = "\033[0m"
r = "\033[31m\033[5m\033[1m"
g = "\033[32m\033[5m\033[1m"


def main() -> None:
    # Parses the given maps
    parse = MapParser()

    if (parse.parse_file() is False):
        raise ValueError
    print(f"{g}[INFO]{end}: Parsing successful!")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"{g}[INFO]{end}: Quitting Fly-in!")
