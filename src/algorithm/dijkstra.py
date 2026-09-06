from heapq import heapify, heappop, heappush
from typing import Any

import numpy as np

from src.objects.zone import Zone

class Dijkstra():
    def __init__(self, zones: dict[str, Zone] = {}):
        self.zones = zones

    def find_shortest(self, start: Zone) -> list[int]:
        """
        This is the algorithm that will be used
        to navigate the drones.

        Parameter:
        - start: Zone

        Return
        -> dict[str, int]
        """
        # Initialize every nodes value to infinity
        dist: dict[str, int] = {node.name: np.inf
                                for name, node in self.zones.items()}
        dist[start] = 0
        visited_nodes: list[int] = []

        # Initialize a priority queue
        priority: list[Any] = [(0, start)]
        heapify(priority)

        # Loops until the priority queue is empty
        while priority:
            curr_dist, curr_node = heappop(priority)

            # Checks whether or not the current node is visited
            if curr_node in visited_nodes:
                continue
            else:
                visited_nodes.append(curr_node)

            # Checks the closest neighbour to the node
            for neighbour, weight in self.zones[curr_node].items():
                calc_dist = curr_dist + weight
                if calc_dist < dist[neighbour]:
                    dist[neighbour] = calc_dist
                    heappush(priority, (calc_dist, neighbour))

        return dist
