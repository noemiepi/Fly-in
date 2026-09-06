from typing import Any

from src.parsing.map_parse import MapParser
from src.algorithm.dijkstra import Dijkstra
from src.ui.visual import Visualizer
from src.ui.menu import UserMenu
from src.monitor import Monitor


end = "\033[0m"
r = "\033[31m\033[5m\033[1m"
g = "\033[32m\033[5m\033[1m"


def main() -> None:
    try:
        # Parses the given maps
        parse = MapParser()
        valid, maps_dict = parse.parse_file()

        if valid is False:
            raise ValueError

    except Exception as e:
        print(f"{r}[ERROR]{end}: An unexpected error occured "
              f"during the parsing:\n-> {e}")
        exit()
    print(f"{g}[INFO]{end}: Parsing successful!")

    # Visualizer
    lvl_name: str = ""
    map_data: dict[str, Any] = {}
    menu: UserMenu = UserMenu(maps_dict)
    lvl_name, map_data = menu.home_menu()

    # Map monitor
    monitor: Monitor = Monitor(map_data)
    monitor.create_level()

    # Starts the algorithm
    algo: Dijkstra = Dijkstra(monitor.zones)
    print(algo.find_shortest(monitor.zones["start"]))

    # Visualizer
    visual: Visualizer = Visualizer(lvl_name.strip(".txt"), monitor)
    visual.start_visual()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{g}[INFO]{end}: Quitting Fly-in!")

    # except Exception as e:
    #     print(f"{r}[ERROR]{end}: An unexpected error occured:\n"
    #           f"-> {e}")
