from typing import Any


class Zone():
    """
    This class will create a zone object.
    """
    def __init__(self, name: str, coords: tuple[int, int],
                 metadata: dict[str, Any]) -> None:
        self.name = name

        self.coords = coords
        self.x: int = 0
        self.y: int = 0
        self.x, self.y = self.coords

        self.zone: str = ""
        self.nb_drones: int = 0
        self.color: str = ""

        for key, value in metadata.items():
            if key == "zone":
                self.zone = value

            if key == "nb_drones":
                self.nb_drones = value

            if key == "color":
                self.color = value
