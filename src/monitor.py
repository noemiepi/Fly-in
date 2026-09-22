import copy

from typing import Any

from src.objects.drone import Drone
from src.objects.zone import Zone
from src.algorithm.dijkstra import Algorithm

end = "\033[0m"
g = "\033[32m\033[5m\033[1m"

MAX_ROUTES: int = 8


class Monitor():
    """
    This class will create every needed objects
    (drones and zones) the level needs.

    Attributes:
      - create_level(self) -> None
      - simulate(self) -> None
      - summary(self) -> str
      - is_over(self) -> bool
      - _plan_routes(self) -> None
      - _give_routes(self, algo: Algorithm,
                     routes: list[dict[str, str]]) -> None
      - _route_rate(self, route: dict[str, str]) -> int
      - _count_turns(self) -> float
      - _flag_finished(self) -> None
      - _remaining(self, drone: Drone) -> int
      - _play_turn(self) -> list[str]
      - _create_drones(self) -> None
      - _create_zones(self) -> None
    """

    def __init__(self, data: dict[str, Any], output: bool) -> None:
        self.level = data
        self.output = output
        self.write_output: str = ""

        self.drones: dict[str, Drone] = {}
        self.zones: dict[str, Zone] = {}
        self.connections: dict[str, Any] = {}

        self.visual_connections: list[tuple[Any, Any]] = []

        self.link_limit: dict[tuple[str, str], int] = {}
        self.zone_limit: dict[str, int] = {}

        self.turn: int = 0
        self.solvable: bool = True

    def create_level(self) -> None:
        """
        Creates the level's objects.
        """
        for hub, data in self.level.items():
            if hub == "connections":
                self.connections = data

        self._create_zones()
        self._create_drones()

        for hub, data in self.level.items():
            if hub == "connections":
                for nb_con, con in data.items():
                    for key, value in con.items():
                        if key == "path":
                            value = value.split("-")
                            from_p: str = value[0]
                            to_p: str = value[1]

                            from_key: str = ""
                            to_key: str = ""

                            for name, zone in self.zones.items():
                                if zone.name == from_p:
                                    from_coords: tuple[int, int] = zone.coords
                                    from_key = name

                                elif zone.name == to_p:
                                    to_coords: tuple[int, int] = zone.coords
                                    to_key = name

                            if not from_key or not to_key:
                                raise ValueError(f"Connection {con['path']} "
                                                 "uses an unknown zone")

                            self.visual_connections.append((from_coords,
                                                            to_coords))
                            self.link_limit[(from_key, to_key)] = \
                                con["nb_drones"]

        # Gives the start point of the drones
        for name, drone in self.drones.items():
            drone.move_to("start")

        self._plan_routes()

        if not self.solvable:
            print("No path between the start and the end")

    def simulate(self) -> None:
        """
        Plays one turn.
        """
        if not self.solvable:
            return

        if self.is_over():
            self._flag_finished()
            return

        moves: list[str] = self._play_turn()
        print(" ".join(moves))
        self.write_output += " ".join(moves)
        self.write_output += "\n"

    def summary(self) -> str:
        """
        Returns the number of turns of the simulation.

        Return
        -> str
        """
        return f"{g}[INFO]{end}: Simulation finished in {self.turn} turns"

    def is_over(self) -> bool:
        """
        Checks if every drone reached the end.

        Return:
        -> bool
        """
        for drone in self.drones.values():
            if drone.get_position() != "end" or drone.transit is not None:
                return False

        return True

    def _plan_routes(self) -> None:
        """
        Looks at the differents routes possibilities and chooses
        the quickest one depending on the zones and link capacity.
        """
        algo: Algorithm = Algorithm(self.zones)
        routes: list[dict[str, str]] = algo.find_routes(MAX_ROUTES)

        if not routes:
            self.solvable = False
            return

        best_nb: int = 1
        best_turns: float = float("inf")

        for nb in range(1, len(routes) + 1):
            trial: Monitor = copy.deepcopy(self)
            trial._give_routes(algo, routes[:nb])
            turns = trial._count_turns()

            if turns < best_turns:
                best_turns = turns
                best_nb = nb

        self._give_routes(algo, routes[:best_nb])

    def _give_routes(
        self, algo: Algorithm, routes: list[dict[str, str]]
    ) -> None:
        """
        Gives a route for each drone.

        Parameters:
          - algo: Algorithm
          - routes: list[dict[str, str]]
        """
        costs: list[float] = [algo.route_cost(route) for route in routes]
        rates: list[int] = [self._route_rate(route) for route in routes]
        sent: list[int] = [0] * len(routes)

        for drone in self.drones.values():
            best: int = 0
            best_arrival: float = float("inf")

            for i in range(len(routes)):
                arrival = costs[i] + sent[i] // rates[i]
                if arrival < best_arrival:
                    best_arrival = arrival
                    best = i

            drone.route = routes[best]
            sent[best] += 1

    def _route_rate(self, route: dict[str, str]) -> int:
        """
        Gives the number of drones that can enter a zone each turn.

        Parameter:
          - route: dict[str, str]

        Return
        -> int
        """
        rate: int = len(self.drones)
        zone: str = "start"

        while zone != "end":
            nxt = route[zone]
            try:
                rate = min(rate, self.link_limit[(zone, nxt)])
            except KeyError:
                rate = min(rate, self.link_limit[(nxt, zone)])

            if nxt != "end":
                rate = min(rate, self.zones[nxt].nb_drones)

            zone = nxt

        return max(rate, 1)

    def _count_turns(self) -> float:
        """
        Counts the number of turns a simulation makes.

        Return
        -> float
        """
        limit: int = 20 * (len(self.zones) + len(self.drones))

        while not self.is_over():
            moves = self._play_turn()

            # In case there are no movements
            if not moves or self.turn > limit:
                return float("inf")

        return self.turn

    def _flag_finished(self) -> None:
        """
        Changes the drone's 'has_finished' variable
        if it reached the end.
        """
        for drone in self.drones.values():
            if drone.get_position() == "end" and drone.transit is None:
                drone.has_finished = True

    def _remaining(self, drone: Drone) -> int:
        """
        Counts the number of zones the drones has to cross.

        Parameter:
          - drone: Drone

        Return
        -> int
        """
        count: int = 0
        zone: str | None = drone.get_position()

        while zone is not None and zone != "end":
            zone = drone.route.get(zone)
            count += 1

        return count

    def _play_turn(self) -> list[str]:
        """
        Moves the drones for one turn.

        Return
        -> list[str]
        """
        self._flag_finished()
        self.turn += 1

        moves: list[str] = []
        link_use: dict[tuple[str, str], int] = {}
        landed: set[str] = set()

        # The drones on a connection have to reach their zone
        for drone_name, drone_obj in self.drones.items():
            if drone_obj.transit is not None:
                link = drone_obj.transit
                link_use[link] = link_use.get(link, 0) + 1

                dest = self.zones[drone_obj.transit[1]].name
                moves.append(f"{drone_obj.id}-{dest}")
                landed.add(drone_obj.id)
                drone_obj.transit = None

        # It will move the drones that are closest to the end first
        order = sorted(self.drones.values(), key=self._remaining)

        for drone_obj in order:
            if drone_obj.has_finished or drone_obj.id in landed:
                continue

            current_name = drone_obj.get_position()
            if current_name is None or current_name == "end":
                continue

            # Look at the next zone on the route
            next_name = drone_obj.route.get(current_name)
            if next_name is None:
                continue

            next_zone: Zone = self.zones[next_name]
            link = (current_name, next_name)

            # Checks that the next zone has room for another drone
            try:
                if link_use.get(link, 0) >= self.link_limit[link]:
                    continue
            except KeyError:
                link = (next_name, current_name)
                if link_use.get(link, 0) >= self.link_limit[link]:
                    continue

            if next_name != "end" and \
               self.zone_limit.get(next_name, 0) >= next_zone.nb_drones:
                continue

            # The drone goes to the next zone
            link_use[link] = link_use.get(link, 0) + 1
            if current_name != "start":
                self.zone_limit[current_name] -= 1

            if next_name != "end":
                self.zone_limit[next_name] = (
                    self.zone_limit.get(next_name, 0) + 1
                )

            drone_obj.move_to(next_name)

            # Handles the restricted zones
            if next_zone.zone == "restricted":
                drone_obj.transit = (current_name, next_name)
                current = self.zones[current_name].name
                moves.append(f"{drone_obj.id}-{current}-{next_zone.name}")

            else:
                moves.append(f"{drone_obj.id}-{next_zone.name}")

        return moves

    def _create_drones(self) -> None:
        """
        Creates and stocks every drones in dictionary.
        """
        nb_drones: int = 0
        i: int = 1

        for key, value in self.level.items():
            if key == "nb_drones":
                nb_drones = value

        while i <= nb_drones:
            self.drones[f"D{i}"] = Drone(i)
            i += 1

    def _create_zones(self) -> None:
        """
        Creates every zones and stocks them in a dictionary.
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

                self.zones["start"] = Zone(
                    name, coords, metadata, self.connections
                )

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

                    self.zones[name] = Zone(
                        name, coords, metadata, self.connections
                    )

            # Creates and stocks the end hub in a dictionary
            if zone == "end_hub":
                for key, value in data.items():
                    if key == "name":
                        name = value

                    if key == "coords":
                        coords = value

                    if key == "metadata":
                        metadata = value

                self.zones["end"] = Zone(
                    name, coords, metadata, self.connections
                )
