from src.objects.zone import Zone


class Drone():
    """
    This class will create a drone object.
    """
    def __init__(self, id: int) -> None:
        self.id = f"D{id}"

        self.curr_pos: str | None = None
        self.visited_zones: list[str] = []
        self.has_finished: bool = False

    def get_position(self) -> str | None:
        return self.curr_pos

    def next_position(self, zone: Zone) -> None:
        self.curr_pos = zone.name
