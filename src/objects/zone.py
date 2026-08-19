from typing import Any


class Zone():
    """
    This class will create a zone object.
    """
    def __init__(self, name: str, coords: tuple[int, int],
                 metadata: dict[str, Any]) -> None:
        self.name = name
        self.coords = coords
        self.metadata = metadata
