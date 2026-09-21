from typing import Any


class Zone:
    """
    This class will create a zone object.
    """

    def __init__(
        self,
        name: str,
        coords: tuple[int, int],
        metadata: dict[str, Any],
        connections: dict[str, Any],
    ) -> None:
        self.name = name

        self.neighbours: list[str] = []

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

        for connection, values in connections.items():
            for key, value in values.items():
                if key == "path":
                    if name in value:
                        steps: list[str] = value.split("-")
                        if steps[0] == name:
                            if (
                                steps[1] == "goal"
                                or steps[1] == "impossible_goal"
                            ):
                                self.neighbours.append("end")

                            else:
                                self.neighbours.append(steps[1])

                        if steps[1] == name:
                            if (
                                steps[0] == "goal"
                                or steps[0] == "impossible_goal"
                            ):
                                self.neighbours.append("end")

                            else:
                                self.neighbours.append(steps[0])
