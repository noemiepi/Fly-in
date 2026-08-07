from src.parsing.map_parse import MapParser
from src.ui.menu import UserMenu


end = "\033[0m"
r = "\033[31m\033[5m\033[1m"
g = "\033[32m\033[5m\033[1m"


def main() -> None:
    try:
        # Parses the given maps
        parse = MapParser()
        valid, maps_dict = parse.parse_file()
        print(maps_dict)

        if (valid is False):
            raise ValueError

    except Exception as e:
        print(f"{r}[ERROR]{end}: An unexpected error occured "
                f"during the parsing:\n-> {e}")
        exit()
    print(f"{g}[INFO]{end}: Parsing successful!")

    # Visualizer
    menu: UserMenu = UserMenu()
    # menu.home_menu(maps_dict)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{g}[INFO]{end}: Quitting Fly-in!")

    except Exception as e:
        print(f"{r}[ERROR]{end}: An unexpected error occured:\n"
                f"-> {e}")
