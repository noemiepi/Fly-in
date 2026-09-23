from typing import Any

from src.parsing.map_parse import MapParser
from src.parsing.arg_parse import arg_parse
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

        # Parses the given arguments
        args = arg_parse()
        arc_visual = args.visual
        output = args.output

    except Exception as e:
        print(f"{r}[ERROR]{end}: An unexpected error occured "
              f"during the parsing:\n-> {e}")
        exit()
    print(f"{g}[INFO]{end}: Parsing successful!")

    # User Menu
    lvl_name: str = ""
    map_data: dict[str, Any] = {}
    menu: UserMenu = UserMenu(maps_dict)
    lvl_name, map_data = menu.home_menu()

    # Map monitor
    monitor: Monitor = Monitor(map_data, output)
    monitor.create_level()

    # Visualizer
    if arc_visual is True:
        visual: Visualizer = Visualizer(lvl_name.strip(".txt"), monitor)
        visual.start_visual()
    else:
        print("Starting simulation\n")
        while monitor.is_over() is False:
            monitor.simulate()
        print(monitor.summary())

    if output is True:
        monitor.write_output += "\nSimulation finished in "
        monitor.write_output += f"{monitor.turn} turns"
        try:
            with open("sim_output.txt", 'w') as f:
                f.write(monitor.write_output)
        except Exception as e:
            raise ValueError(f"The output writing had an issue: {e}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{g}[INFO]{end}: Quitting Fly-in!")

    except Exception as e:
        print(f"{r}[ERROR]{end}: An unexpected error occured:\n-> {e}")
