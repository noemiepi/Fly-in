from heapq import heapify, heappop, heappush
from typing import Any

import numpy as np

from src.objects.zone import Zone

ROUTE_PENALTY: float = 1


class Algorithm():
    """
    This is the class for the algorithm and a scheduler
    that will be used to navigate the drones.

    Attributes:
    - dijkstra(self) -> dict[str, float]
    - find_next_step(self, predecessors: dict[str, Any],
                     distances: dict[str, float]) -> list[str]
    """

    def __init__(self, zones: dict[str, Zone]) -> None:
        self.zones = zones
        self.zone_weight: dict[str, float] = {}
        self.penalty: dict[str, float] = {}
        self.link_penalty: dict[Any, float] = {}

        self.key_of: dict[str, str] = {}
        for key, zone in self.zones.items():
            self.key_of[zone.name] = key

        # Defines the weight of each zone
        for name, zone in self.zones.items():
            if zone.zone == "normal":
                self.zone_weight[name] = 1

            elif zone.zone == "blocked" or name == "start":
                self.zone_weight[name] = np.inf

            elif zone.zone == "restricted":
                self.zone_weight[name] = 2

            elif zone.zone == "priority":
                self.zone_weight[name] = 0.9

            else:
                self.zone_weight[name] = 1

    def dijkstra(self) -> dict[str, str]:
        """
        This is the algorithm that will be used
        to navigate the drones.

        Return
        -> dict[str, str]
        """
        # Initialize every nodes value to infinity
        dist: dict[str, float] = {}
        predecessors: dict[str, Any] = {}

        for key in self.zones:
            dist[key] = np.inf
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
            for name in self.zones[curr_node].neighbours:
                neighbour = self.key_of.get(name, name)
                weight = (
                    self.zone_weight[neighbour]
                    + self.penalty.get(neighbour, 0)
                    + self.link_penalty.get((curr_node, neighbour), 0)
                )

                calc_dist = curr_dist + weight
                if calc_dist < dist[neighbour]:
                    dist[neighbour] = calc_dist
                    predecessors[neighbour] = curr_node
                    heappush(priority, (calc_dist, neighbour))

        # Searches the quickest route from the start to the end
        path: list[str] = self.find_next_step(predecessors, dist)

        next_step: dict[str, str] = {}
        for i in range(len(path) - 1):
            next_step[path[i]] = path[i + 1]

        return next_step

    def find_next_step(
        self, predecessors: dict[str, Any], distances: dict[str, float]
    ) -> list[str]:
        """
        Searches the quickest route to go from the start to the end.

        Parameter:
          - predecessors: dict[str, Any]
          - distances: dict[str, float]

        Return
        -> list[str]
        """
        if distances.get("end") == np.inf:
            return []

        path: list[str] = ["end"]
        node: str = "end"

        while node != "start":
            node = predecessors[node]
            path.append(node)

        path.reverse()

        return path

    def find_routes(self, nb_routes: int) -> list[dict[str, str]]:
        """
        Runs Dijkstraa few times to get different routes.
        The zones found previously gets a penalty to gather each route.

        Parameter
          - nb_routes: int

        Return
        -> list[dict[str, str]]
        """
        routes: list[dict[str, str]] = []

        for _ in range(nb_routes * 2):
            route = self.dijkstra()

            if not route:
                break

            if route not in routes:
                routes.append(route)
                if len(routes) == nb_routes:
                    break

            for zone, next_zone in route.items():
                link = (zone, next_zone)
                self.link_penalty[link] = (self.link_penalty.get(zone, 0) +
                                           ROUTE_PENALTY)

                if zone != "start":
                    self.penalty[zone] = (self.penalty.get(zone, 0) +
                                          ROUTE_PENALTY)

        self.penalty = {}
        self.link_penalty = {}

        routes.sort(key=self.route_cost)

        return routes

    def route_cost(self, route: dict[str, str]) -> float:
        """
        The number of turns a drones has to do to follow the route.

        Parameter:
          - route: dict[str, str]

        Return
        -> float
        """
        cost: float = 0
        zone: str = "start"

        while zone != "end":
            zone = route[zone]

            if self.zones[zone].zone == "restricted":
                cost += 2

            else:
                cost += 1

        return cost
