from src.objects.zone import Zone


class Drone():
    """
    This class will create a drone object.

    Attributes:
      - get_position(self) -> str | None
      - next_position(self, zone: Zone) -> None
      - move_to(self, zone: str) -> None
    """

    def __init__(self, id: int) -> None:
        self.id = f"D{id}"

        self.curr_pos: str | None = None
        self.visited_zones: list[str] = []
        self.has_finished: bool = False

        self.route: dict[str, str] = {}
        self.transit: tuple[str, str] | None = None

    def get_position(self) -> str | None:
        """
        Returns the current position of the drone.

        Return
          -> str | None
        """
        return self.curr_pos

    def next_position(self, zone: Zone) -> None:
        """
        Updates the drone's current position.

        Parameter:
          - zone: Zone
        """
        self.curr_pos = zone.name

    def move_to(self, zone: str) -> None:
        """
        Moves the drone to a one and updates the
        list of visited zones.

        Parameter:
          - zone: str
        """
        self.curr_pos = zone
        self.visited_zones.append(zone)
