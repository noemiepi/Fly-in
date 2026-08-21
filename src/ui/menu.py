import os
import time

from typing import Any

from src.parsing.map_parse import MapParser


end = "\033[0m"
r = "\033[31m\033[5m\033[1m"
g = "\033[32m\033[5m\033[1m"


class UserMenu():
    """
    This class shows the user menu to select a map for the simulaton.

    Attributes:
      - home_menu(self) -> dict[str, Any]
      - easy_maps(self) -> dict[str, Any]
      - normal_maps(self) -> dict[str, Any]
      - hard_maps(self) -> dict[str, Any]
      - hardcore_maps(self) -> dict[str, Any]
      - creative_maps(self) -> dict[str, Any]
    """
    def __init__(self, maps_dict: dict[str, dict[str, Any]]) -> None:
        map_parse: MapParser = MapParser()

        file_list: list[str] = map_parse.filelist
        sorted_file_list: list[str] = sorted(file_list)

        self.maps_dict = maps_dict

        # Sorts maps by difficulty
        self.map_name_dict: dict[str, list[Any]] = {}

        for file in sorted_file_list:
            path = file.split("/")
            folder = path[2]
            name = path[3]

            if folder not in self.map_name_dict:
                self.map_name_dict[folder] = []

            for key, value in self.map_name_dict.items():
                if key == folder:
                    value.append(name)

    def home_menu(self) -> dict[str, Any]:
        """
        Displays the main menu with each map's difficulty.

        Return
            -> dict[str, Any]
        """
        map_data: dict[str, Any] = {}

        os.system('clear')
        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔═════════| Fly-in Menu |═════════╗")
        print("     ║Please choose a difficulty:      ║")
        print("     ║   1- Easy                       ║")
        print("     ║   2- Normal                     ║")
        print("     ║   3- Hard                       ║")
        print("     ║   4- Hardcore                   ║")
        print("     ║   5- Creative                   ║")
        print("     ║   6- Quit                       ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input("\nMake a choice (1-6): "))

            if not 1 <= choice <= 6:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      "Please select a number between 1 and 6")
                time.sleep(1)
                self.home_menu()

            elif choice == 1:
                os.system('clear')
                map_data = self.easy_maps()

            elif choice == 2:
                os.system('clear')
                map_data = self.normal_maps()

            elif choice == 3:
                os.system('clear')
                map_data = self.hard_maps()

            elif choice == 4:
                os.system('clear')
                map_data = self.hardcore_maps()

            elif choice == 5:
                os.system('clear')
                map_data = self.creative_maps()

            elif choice == 6:
                print("\n             Exiting the program...")
                print("                 Goodbye! :D")

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")

        return map_data

    def easy_maps(self) -> dict[str, Any]:
        """
        Displays the easy map(s) to select.

        Return
            -> dict[str, Any]
        """
        line: str = ""
        space: str = ""

        lenght: int = 0
        i: int = 0

        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔══════════| Easy Maps |══════════╗")
        print("     ║Please choose a level:           ║")
        for folder, level in self.map_name_dict.items():
            if folder == "easy":
                while i < len(level):
                    if len(level[i]) > 27:
                        level[i] = level[i][:21]
                        level[i] += "...txt"

                    line = f"║ {i + 1}- {level[i]}"
                    lenght = len(line)
                    space = ""

                    if lenght != 35:
                        while lenght < 34:
                            space += " "
                            lenght += 1
                        space += "║"
                    print(f"     {line + space}")
                    i += 1

        i += 1
        print(f"     ║ {i}- Exit                         ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input(f"\nMake a choice (1-{i}): "))

            if not 1 <= choice <= i:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      f"Please select a number between 1 and {i}")
                time.sleep(1)
                self.home_menu()

            elif choice == i:
                os.system('clear')
                self.home_menu()

            else:
                for folder, maps in self.maps_dict.items():
                    for folder, level in self.map_name_dict.items():
                        if folder == "easy":
                            for name, info in maps.items():
                                if name == level[choice - 1]:
                                    return info

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")

    def normal_maps(self) -> dict[str, Any]:
        """
        Displays the normal map(s) to select.

        Return
            -> dict[str, Any]
        """
        line: str = ""
        space: str = ""

        lenght: int = 0
        i: int = 0

        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔═════════| Normal Maps |═════════╗")
        print("     ║Please choose a level:           ║")
        for folder, level in self.map_name_dict.items():
            if folder == "medium":
                while i < len(level):
                    if len(level[i]) > 27:
                        level[i] = level[i][:21]
                        level[i] += "...txt"

                    line = f"║ {i + 1}- {level[i]}"
                    lenght = len(line)
                    space = ""

                    if lenght != 35:
                        while lenght < 34:
                            space += " "
                            lenght += 1
                        space += "║"
                    print(f"     {line + space}")
                    i += 1

        i += 1
        print(f"     ║ {i}- Exit                         ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input(f"\nMake a choice (1-{i}): "))

            if not 1 <= choice <= i:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      f"Please select a number between 1 and {i}")
                time.sleep(1)
                self.home_menu()

            elif choice == i:
                os.system('clear')
                self.home_menu()

            else:
                for folder, maps in self.maps_dict.items():
                    for folder, level in self.map_name_dict.items():
                        if folder == "medium":
                            for name, info in maps.items():
                                if name == level[choice - 1]:
                                    return info

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")

    def hard_maps(self) -> dict[str, Any]:
        """
        Displays the hard map(s) to select.

        Return
            -> dict[str, Any]
        """
        line: str = ""
        space: str = ""

        lenght: int = 0
        i: int = 0

        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔══════════| Hard Maps |══════════╗")
        print("     ║Please choose a level:           ║")
        for folder, level in self.map_name_dict.items():
            if folder == "hard":
                while i < len(level):
                    if len(level[i]) > 27:
                        level[i] = level[i][:21]
                        level[i] += "...txt"

                    line = f"║ {i + 1}- {level[i]}"
                    lenght = len(line)
                    space = ""

                    if lenght != 35:
                        while lenght < 34:
                            space += " "
                            lenght += 1
                        space += "║"
                    print(f"     {line + space}")
                    i += 1

        i += 1
        print(f"     ║ {i}- Exit                         ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input(f"\nMake a choice (1-{i}): "))

            if not 1 <= choice <= i:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      f"Please select a number between 1 and {i}")
                time.sleep(1)
                self.home_menu()

            elif choice == i:
                os.system('clear')
                self.home_menu()

            else:
                for folder, maps in self.maps_dict.items():
                    for folder, level in self.map_name_dict.items():
                        if folder == "hard":
                            for name, info in maps.items():
                                if name == level[choice - 1]:
                                    return info

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")

    def hardcore_maps(self) -> dict[str, Any]:
        """
        Displays the challenger map(s) to select.

        Return
            -> dict[str, Any]
        """
        line: str = ""
        space: str = ""

        lenght: int = 0
        i: int = 0

        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔════════| Hardcore Maps |════════╗")
        print("     ║Please choose a level:           ║")
        for folder, level in self.map_name_dict.items():
            if folder == "challenger":
                while i < len(level):
                    if len(level[i]) > 27:
                        level[i] = level[i][:21]
                        level[i] += "...txt"

                    line = f"║ {i + 1}- {level[i]}"
                    lenght = len(line)
                    space = ""

                    if lenght != 35:
                        while lenght < 34:
                            space += " "
                            lenght += 1
                        space += "║"
                    print(f"     {line + space}")
                    i += 1

        i += 1
        print(f"     ║ {i}- Exit                         ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input(f"\nMake a choice (1-{i}): "))

            if not 1 <= choice <= i:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      f"Please select a number between 1 and {i}")
                time.sleep(1)
                self.home_menu()

            elif choice == i:
                os.system('clear')
                self.home_menu()

            else:
                for folder, maps in self.maps_dict.items():
                    for folder, level in self.map_name_dict.items():
                        if folder == "challenger":
                            for name, info in maps.items():
                                if name == level[choice - 1]:
                                    return info

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")

    def creative_maps(self) -> dict[str, Any]:
        """
        Displays the custom map(s) to select.

        Return
            -> dict[str, Any]
        """
        line: str = ""
        space: str = ""

        lenght: int = 0
        i: int = 0

        print()
        print("███████╗██╗  ██╗     ██╗     ██████╗██╗   ██╗")
        print("██╔════╝██║  ╚═██╗ ██╔═╝       ██╔═╝████╗ ██║")
        print("█████╗  ██║    ╚═██╔═╝ █████╗  ██║  ██╔═████║")
        print("██╔══╝  ██║      ██║   ╚════╝  ██║  ██║ ╚═██║")
        print("██║     ███████╗ ██║         ██████╗██║   ██║")
        print("╚═╝     ╚══════╝ ╚═╝         ╚═════╝╚═╝   ╚═╝")

        print("\n     ╔════════| Creative Maps |════════╗")
        print("     ║Please choose a level:           ║")
        for folder, level in self.map_name_dict.items():
            if folder == "custom":
                while i < len(level):
                    if len(level[i]) > 27:
                        level[i] = level[i][:21]
                        level[i] += "...txt"

                    line = f"║ {i + 1}- {level[i]}"
                    lenght = len(line)
                    space = ""

                    if lenght != 35:
                        while lenght < 34:
                            space += " "
                            lenght += 1
                        space += "║"
                    print(f"     {line + space}")
                    i += 1

        i += 1
        print(f"     ║ {i}- Exit                         ║")
        print("     ╚═════════════════════════════════╝")

        try:
            choice = int(input(f"\nMake a choice (1-{i}): "))

            if not 1 <= choice <= i:
                print(f"\n{r}[ERROR]{end}: Invalid choice! "
                      f"Please select a number between 1 and {i}")
                time.sleep(1)
                self.home_menu()

            elif choice == i:
                os.system('clear')
                self.home_menu()

            else:
                for folder, maps in self.maps_dict.items():
                    for folder, level in self.map_name_dict.items():
                        if folder == "custom":
                            for name, info in maps.items():
                                if name == level[choice - 1]:
                                    return info

        except ValueError:
            print(f"\n{r}[ERROR]{end}: You didn't enter an int")
            time.sleep(1)
            self.home_menu()

        except Exception as e:
            os.system('clear')
            print(f"\n{e}")
