from typing import Any

import numpy as np

from src.objects.zone import Zone

def dijkstra(nodes: dict[str, Zone], connections: dict[str, Any],
             start: Zone) -> list[int]:
    """
    This is the algorithm that will be used
    to navigate the drones.

    Parameters:
      - nodes: dict[str, Zone]
      - connections: dict[str, Any]
      - start: Zone

    Return
      -> list[int]
    """
    dist: list[int] = [np.inf] * len(nodes)
    dist[0] = 0
    visited_nodes: list[int] = []
    pass
