import re
import sys
import glob

end = "\033[0m"
r = "\033[31m\033[5m\033[1m"


class MapParser():
    """
    This class will parse every map file present in the maps subfolders.

    Attributes:
      - is_valid(self, data: str) -> bool
    """
    def __init__(self) -> None:
        try:
            # Reunites every files in maps folder
            self.filelist = glob.glob("data/maps/**/*.txt", recursive=True)

        except PermissionError:
            raise ValueError

        except FileNotFoundError:
            raise ValueError

    def parse_file(self) -> bool:
        """
        Parse every map files.

        Return
            -> bool
        """
        # Checks every file one by one
        for file in self.filelist:
            if (self.is_valid(file) is False):
                return False

        return True

    def is_valid(self, file: str) -> bool:
        """
        Checks if the file has the correct configuration
        for the steps definitions and the drones.

        Parameter:
          - data: str

        Return
          -> bool
        """
        keyword: list[str] = ["nb_drones", "start_hub", "end_hub",
                              "hub", "connection"]

        first: bool = True
        start_hub: int = 0
        end_hub: int = 0

        try:
            with open(file, "r") as f:
                for i, line in enumerate(f, 1):
                    line = line.split("#", 1)[0].strip()

                    # Doesn't count comment and empty line
                    if line.startswith("#") or not line:
                        continue

                    key, value = line.split(":", 1)
                    key = key.strip()

                    # Checks if the correct keywords are used
                    if key not in keyword:
                        raise ValueError(f"{r}[ERROR]{end}: An invalid "
                                         f"keyword is used (l.{i})")

                    if first:
                        if key != "nb_drones":
                            raise ValueError(f"{r}[ERROR]{end}: Number "
                                             "of drones isn't the first "
                                             f"parameter (l.{i})")
                        first = False

                    # Checks the steps and their validity
                    value = value.strip()
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
                                meta_keyword = meta.split("=")[0]
                                if meta_keyword not in ["zone", "color",
                                                        "max_drones"]:
                                    raise ValueError(f"{r}[ERROR]{end}: "
                                                     "Invalid given keyword "
                                                     "for the metadata "
                                                     f"(l.{i})")

                                meta_value = meta.split("=")[1]
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

                                if meta_keyword == "color":
                                    if " " in meta_value or "-" in meta_value \
                                     or "_" in meta_value:
                                        raise ValueError(f"{r}[ERROR]{end}: "
                                                         "Invalid color name "
                                                         f"(l.{i})")

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

                    # Checks the connections and their validity
                    if key == "connection":
                        if "-" in value:
                            path = value.split(" ")[0]

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

            if start_hub == 0:
                raise ValueError(f"{r}[ERROR]{end}: No start_hub detected")

            if end_hub == 0:
                raise ValueError(f"{r}[ERROR]{end}: No end_hub detected")

        except FileNotFoundError:
            raise ValueError(f"{r}[ERROR]{end}: File not found")

        except PermissionError:
            raise ValueError(f"{r}[ERROR]{end}: Lack permission to "
                             "open the file")

        except Exception as e:
            print(e)
            sys.exit()

        return True
