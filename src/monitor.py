from typing import Any

from src.objects.drone import Drone
from src.objects.zone import Zone


class Monitor():
    """
    This class will create every needed objects
    (drones and zones) the level needs.

    Attributes:
      - create_level(self) -> None
      - _create_drones(self) -> None
      - _create_zones(self) -> None
    """
    def __init__(self, data: dict[str, Any]) -> None:
        self.level = data

        self.drones: dict[str, Drone] = {}
        self.zones: dict[str, Zone] = {}

    def create_level(self) -> None:
        """
        Creates the level's object.

        Return
            -> None
        """
        self._create_drones()
        self._create_zones()

    def _create_drones(self) -> None:
        """
        Creates and stocks every drones in dictionary.

        Return
            -> None
        """
        nb_drones: int = 0
        i: int = 1

        for key, value in self.level.items():
            if key == "nb_drones":
                nb_drones = value

        while (i <= nb_drones):
            self.drones[f"D{i}"] = Drone(i)
            i += 1

    def _create_zones(self) -> None:
        """
        Creates every zones and stocks them in a dictionary.

        Return
            -> None
        """
        for zone, data in self.level.items():
            # Creates and stocks the start hub in a dictionary
            if zone == "start_hub":
                for key, value in data.items():
                    if key == "name":
                        name: str = value

                    if key == "coords":
                        coords: tuple[int, int] = value

                    if key == "metadata":
                        metadata: dict[str, Any] = value

                    self.zones["start"] = Zone(name, coords, metadata)

            # Creates and stocks the end hub in a dictionary
            if zone == "end_hub":
                for key, value in data.items():
                    if key == "name":
                        name = value

                    if key == "coords":
                        coords = value

                    if key == "metadata":
                        metadata = value

                    self.zones["end"] = Zone(name, coords, metadata)

            # Creates and stocks the hubs in a dictionary
            if zone == "hubs":
                for hubs, hubs_data in data.items():
                    for hub_id, hub_data in hubs_data.items():
                        for key, value in hub_data.items():
                            if key == "name":
                                name = value

                            if key == "coords":
                                coords = value

                            if key == "metadata":
                                metadata = value

                            self.zones[hub_id] = Zone(name, coords, metadata)
