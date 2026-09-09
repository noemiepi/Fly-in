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
        self.connections: dict[str, Any] = {}

        self.visual_connections: list[tuple[Any, Any]] = []

    def create_level(self) -> None:
        """
        Creates the level's object.

        Return
            -> None
        """
        for hub, data in self.level.items():
            if hub == "connections":
                self.connections = data

        self._create_drones()
        self._create_zones()

        for hub, data in self.level.items():
            if hub == "connections":
                for nb_con, con in data.items():
                    for key, value in con.items():
                        if key == "path":
                            value = value.split("-")
                            from_p: str = value[0]
                            to_p: str = value[1]

                            for name, zone in self.zones.items():
                                if zone.name == from_p:
                                    from_coords: tuple[int, int] = zone.coords

                                elif zone.name == to_p:
                                    to_coords: tuple[int, int] = zone.coords

                            self.visual_connections.append((from_coords,
                                                            to_coords))

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
        name: str = ""
        coords: tuple[int, int]
        metadata: dict[str, Any] = {}

        for zone, data in self.level.items():
            # Creates and stocks the start hub in a dictionary
            if zone == "start_hub":
                for key, value in data.items():
                    if key == "name":
                        name = value

                    if key == "coords":
                        coords = value

                    if key == "metadata":
                        metadata = value

                self.zones[name] = Zone(name, coords,
                                        metadata,
                                        self.connections)

            # Creates and stocks the hubs in a dictionary
            if zone == "hubs":
                for hubs, hub_data in data.items():
                    for hub_id, value in hub_data.items():
                        if hub_id == "name":
                            name = value

                        if hub_id == "coords":
                            coords = value

                        if hub_id == "metadata":
                            metadata = value

                    self.zones[name] = Zone(name, coords,
                                            metadata,
                                            self.connections)

            # Creates and stocks the end hub in a dictionary
            if zone == "end_hub":
                for key, value in data.items():
                    if key == "name":
                        name = value

                    if key == "coords":
                        coords = value

                    if key == "metadata":
                        metadata = value

                self.zones["end"] = Zone(name, coords,
                                        metadata,
                                        self.connections)
