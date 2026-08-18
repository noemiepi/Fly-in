import re
import glob

from typing import Any

r = "\033[31m\033[5m\033[1m"
end = "\033[0m"


class MapParser():
    """
    This class will parse every map file present in the maps subfolders.

    Attributes:
      - parse_file(self) -> tuple[bool, dict[str, list[Any]]]
      - is_valid(self, file: str) -> tuple[bool, list[Any]]
    """
    def __init__(self) -> None:
        try:
            # Reunites every files in maps folder
            self.filelist: list[str] = glob.glob("data/maps/**/*.txt",
                                                 recursive=True)

        except PermissionError:
            raise ValueError

        except FileNotFoundError:
            raise ValueError

    def parse_file(self) -> bool | \
            tuple[bool, dict[str, dict[str, dict[str, Any]]]]:
        """
        Parse every map files.

        Return
            -> bool | tuple[bool, dict[str, list[Any]]]
        """
        maps_dict: dict[str, dict[str, dict[str, Any]]] = {}
        level_dict: dict[str, Any] = {}

        path: list[str] = []
        name: str = ""

        valid: bool = False

        # Checks every file one by one
        for file in self.filelist:
            valid, level_dict = self.is_valid(file)

            if valid is False:
                return False

            # Adds the map's informations in a dictionary with the map's name
            path = file.split("/")
            name = path[3]
            folder = path[2]

            maps_dict.setdefault(folder, {name: level_dict})

            for key, value in maps_dict.items():
                if key == folder:
                    value.update({name: level_dict})

        return (True, maps_dict)

    def is_valid(self, file: str) -> tuple[bool, dict[str, Any]]:
        """
        Checks if the file has the correct configuration
        for the steps definitions and the drones.

        Parameter:
          - file: str

        Return
          -> tuple[bool, dict[str, Any]]
        """
        level_dict: dict[str, Any] = {}
        hub_dict: dict[str, Any] = {}
        connect_dict: dict[str, Any] = {}
        keyword: list[str] = ["nb_drones", "start_hub", "end_hub",
                              "hub", "connection"]

        first: bool = True
        start_hub: int = 0
        end_hub: int = 0

        zone: str = ""
        color: str | None = ""
        nb_drone: int = 0

        j: int = 1
        k: int = 1

        try:
            with open(file, "r") as f:
                for i, line in enumerate(f, 1):
                    line = line.split("#", 1)[0].strip()

                    # Doesn't count comment and empty line
                    if line.startswith("#") or not line:
                        continue

                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    # Checks if the correct keywords are used
                    if key not in keyword:
                        raise ValueError(f"{r}[ERROR]{end}: An invalid "
                                         f"keyword is used (l.{i})")

                    if first:
                        if key != "nb_drones":
                            raise ValueError(f"{r}[ERROR]{end}: Number "
                                             "of drones isn't the first "
                                             f"parameter (l.{i})")

                        try:
                            nb_drone = int(value)

                        except ValueError:
                            raise ValueError(f"{r}[ERROR]{end}: Invalid drone "
                                             "number. It should be an integer"
                                             f"(l.{i})")

                        if nb_drone <= 0:
                            raise ValueError(f"{r}[ERROR]{end}: Invalid number"
                                             " of drones (Needs to be above 0)"
                                             f" (l.{i})")

                        level_dict["nb_drones"] = nb_drone
                        first = False

                    # Checks the steps and their validity
                    if key in ["start_hub", "end_hub", "hub"]:
                        if key == "start_hub":
                            start_hub += 1
                            if start_hub > 1:
                                raise ValueError(f"{r}[ERROR]{end}: Over one "
                                                 "start_hub contain a dash "
                                                 f"(l.{i})")

                        if key == "end_hub":
                            end_hub += 1
                            if end_hub > 1:
                                raise ValueError(f"{r}[ERROR]{end}: Over one "
                                                 "end_hub contain a dash "
                                                 f"(l.{i})")

                        name = value.split(" ")[0]
                        if "-" in name or " " in name:
                            raise ValueError(f"{r}[ERROR]{end}: {name} is an "
                                             "invalid name. It shouldn't "
                                             f"contain a dash (l.{i})")

                        x = value.split(" ")[1]
                        y = value.split(" ")[2]
                        try:
                            nx = int(x)
                            ny = int(y)

                        except ValueError:
                            raise ValueError(f"{r}[ERROR]{end}: Invalid "
                                             "given coordinates. They "
                                             f"should be integers (l.{i})")

                        metadata = re.findall(r'\[(.+)\]', value)
                        if metadata:
                            meta_name = metadata[0].split()
                            for meta in meta_name:
                                meta_keyword: str = meta.split("=")[0]
                                if meta_keyword not in ["zone", "color",
                                                        "max_drones"]:
                                    raise ValueError(f"{r}[ERROR]{end}: "
                                                     "Invalid given keyword "
                                                     "for the metadata "
                                                     f"(l.{i})")

                                meta_value: str = meta.split("=")[1]
                                meta_value = meta_value.strip()
                                if meta_keyword == "zone":
                                    if meta_value not in ["normal",
                                                          "blocked",
                                                          "restricted",
                                                          "priority"]:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid value "
                                                         "for the zone "
                                                         f"(l.{i})")
                                    zone = meta_value

                                if meta_keyword == "color":
                                    if " " in meta_value or "-" in meta_value \
                                     or "_" in meta_value:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid color name "
                                                         f"(l.{i})")
                                    color = meta_value

                                if meta_keyword == "max_drones":
                                    try:
                                        nb_drone = int(meta_value)

                                    except ValueError:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid drone "
                                                         "number. It should "
                                                         "be an integers"
                                                         f"(l.{i})")

                                    if nb_drone <= 0:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid number of "
                                                         "drones (Needs to be"
                                                         f" above 0) (l.{i})")

                        # Stocks the data in a dictionary
                        if zone == "":
                            zone = "normal"

                        if nb_drone == 0:
                            nb_drone = 1

                        if color == "":
                            color = None

                        if key == "start_hub":
                            level_dict["start_hub"] = {"name": name,
                                                       "coords": (nx, ny),
                                                       "metadata": [color]}

                        if key == "end_hub":
                            level_dict["end_hub"] = {"name": name,
                                                     "coords": (nx, ny),
                                                     "metadata": [color]}

                        if key not in ["start_hub", "end_hub"]:
                            hub_dict.update({f"hub{j}": {
                                "name": name,
                                "coords": (nx, ny),
                                "metadata": {
                                    "zone": zone,
                                    "nb_drones": nb_drone,
                                    "color": color
                                            }
                                            }})

                            j += 1

                    nb_drone = 0

                    # Checks the connections and their validity
                    if key == "connection":
                        if "-" in value:
                            path: str = value.split(" ")[0]

                            metadata = re.findall(r'\[(.+)\]', value)
                            if metadata:
                                meta_name = metadata[0].split()
                                for meta in meta_name:
                                    meta_keyword = meta.split("=")[0]
                                    if meta_keyword != "max_link_capacity":
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid metadata "
                                                         f"keyword (l.{i})")

                                    meta_value = meta.split("=")[1]
                                    meta_value = meta_value.strip()
                                    try:
                                        nb_drone = int(meta_value)

                                    except ValueError:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid drone "
                                                         "number. It should "
                                                         "be an integers"
                                                         f"(l.{i})")

                                    if nb_drone <= 0:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid number of "
                                                         "drones (Needs to "
                                                         "be above 0)"
                                                         f"(l.{i})")

                        if nb_drone == 0:
                            nb_drone = 1

                        # Stocks the data in a dictionary
                        connect_dict.update({f"connection{k}":
                                             {"path": path,
                                              "nb_drones": nb_drone}})
                        k += 1

            # Adds the zones and their connections to the level's dictionary
            level_dict["hubs"] = hub_dict
            level_dict["connections"] = connect_dict

            # Checks if there's a start and an end
            if start_hub == 0:
                raise ValueError(f"{r}[ERROR]{end}: No start_hub detected")

            if end_hub == 0:
                raise ValueError(f"{r}[ERROR]{end}: No end_hub detected")

        except FileNotFoundError:
            raise ValueError(f"{r}[ERROR]{end}: File not found")

        except PermissionError:
            raise ValueError(f"{r}[ERROR]{end}: Lack permission to "
                             "open the file")

        return (True, level_dict)
