from heapq import heapify, heappop, heappush
from typing import Any

import numpy as np

from src.objects.zone import Zone


class Algorithm():
    """
    This is the class for the algorithm and a scheduler 
    that will be used to navigate the drones.

    Attributes:
    - dijkstra(self) -> dict[str, float]
    - scheduler(self) -> None
    """
    def __init__(self, zones: dict[str, Zone] = {}):
        self.zones = zones
        self.zone_weight: dict[str, float] = {}

        for name, zone in self.zones.items():
            for neighbour in zone.neighbours:
                for name, zone in self.zones.items():
                    if zone.name == neighbour:
                        if zone.zone == "normal":
                            self.zone_weight[zone.name] = 1

                        if zone.zone == "blocked":
                            self.zone_weight[zone.name] = np.inf

                        if zone.zone == "restricted":
                            self.zone_weight[zone.name] = 4

                        if zone.zone == "priority":
                            self.zone_weight[zone.name] = 2

                        if zone.name == "start":
                            self.zone_weight[zone.name] = np.inf

                if neighbour == "end":
                    self.zone_weight["end"] = 1

    def dijkstra(self) -> dict[str, float]:
        """
        This is the algorithm that will be used
        to navigate the drones.

        Return
        -> dict[str, float]
        """
        # Initialize every nodes value to infinity
        dist: dict[str, float] = {}
        for name, node in self.zones.items():
            if node.name == "goal" or node.name == "impossible_goal":
                dist["end"] = np.inf
            else:
                dist[node.name] = np.inf
        dist["start"] = 0

        visited_nodes: list[int] = []

        # Initialize a priority queue
        priority: list[Any] = [(0, "start")]
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
            for neighbour in self.zones[curr_node].neighbours:
                for name, weight in self.zone_weight.items():
                    if name == neighbour:
                        calc_dist = curr_dist + weight
                        if calc_dist < dist[neighbour]:
                            dist.update({neighbour: calc_dist})
                            heappush(priority, (calc_dist, neighbour))

        return dist

    def scheduler(self) -> None:
        """
        This is the scheduler that will give the priority
        order when not every drone can go to a zone.

        Return
        -> dict[str, float]
        """
