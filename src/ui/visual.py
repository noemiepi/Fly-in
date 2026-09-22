import os
import time
import math
import arcade
import random

from src.monitor import Monitor
from src.ui.utils.icon import Icon
from src.ui.utils.color import Color
from src.ui.utils.text_outline import OutlinedText

# --- CONSTANTS --- #
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 900
TITLE = "Fly-in 🌻🐝"

BACK_PATH = "assets/background/"
START_END_PATH = "assets/start-end/"
HUB_PATH = "assets/steps/"
DRONE_PATH = "assets/drones/"

MUSIC_PATH = "assets/music/"
FONT_PATH = "assets/font/"

SCALE = 0.5
SPRITE_SIZE = 256
MARGIN = 150
DRONE_SPEED = 200
# ----------------- #


class Visualizer(arcade.Window):
    """
    This class will create a window in which
    there will be a visual of the map.

    Attributes:
      - setup(self) -> None
      - on_draw(self) -> None
      - start_visual(self) -> None
      - on_key_press(self, key: int, _modifiers: int) -> None
      - _build_zone(self, name: str, zone: str, x: int, y: int) -> None
      - _build_connections(self) -> None
      - _load_sprites(self) -> None
    """

    def __init__(self, lvl_name: str, monitor: Monitor) -> None:
        super().__init__(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            title=TITLE,
            resizable=True,
            center_window=True,
        )

        self.background_color = arcade.color.BLUE_BELL

        self.lvl_name = lvl_name
        self.monitor = monitor

        self.setup()
        self._is_sim_started: bool = False
        self._is_moving: bool = False

    def setup(self) -> None:
        """
        Initializes the visual.
        """
        self.zone_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.drone_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.connection_list: arcade.shape_list.ShapeElementList[
            arcade.shape_list.Shape
        ] = arcade.shape_list.ShapeElementList()

        self.legend_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.text_list: list[arcade.Text] = []
        self.turn_text: arcade.Text

        # Loads the text font
        arcade.load_font(f"{FONT_PATH}MinecraftFont.woff")

        text = OutlinedText(
            text=self.lvl_name,
            x=WINDOW_WIDTH / 2,
            y=WINDOW_HEIGHT - 50,
            color=arcade.color.WHITE,
            font_size=25,
            anchor_x="center",
            font_name="Minecraft",
        )
        self.text_list.append(text)

        self.turn_text = OutlinedText(
            text="Turn 0",
            x=75,
            y=40,
            color=arcade.color.WHITE,
            font_size=13,
            anchor_x="center",
            font_name="Minecraft",
        )

        # Adapts the scale depending on the map size
        x_lst: list[int] = [data.x for data in self.monitor.zones.values()]
        y_lst: list[int] = [data.y for data in self.monitor.zones.values()]
        min_x, max_x = min(x_lst), max(x_lst)
        min_y, max_y = min(y_lst), max(y_lst)

        width_units = max_x - min_x
        height_units = max_y - min_y

        avail_w = WINDOW_WIDTH - 2 * MARGIN
        avail_h = WINDOW_HEIGHT - 2 * MARGIN
        spacing_x = avail_w / width_units if width_units else SPRITE_SIZE
        spacing_y = avail_h / height_units if height_units else SPRITE_SIZE

        self.spacing: float | int = min(spacing_x, spacing_y, SPRITE_SIZE)
        self.sprite_scale: float | int = min(SCALE, self.spacing / SPRITE_SIZE)
        self.center_gx: float = (min_x + max_x) / 2
        self.center_gy: float = (min_y + max_y) / 2

        self._load_sprites()

        # Creates the legend
        count: int = 1
        legend_sprite: dict[str, arcade.Texture | str] = {
            "Start": f"{START_END_PATH}start.png",
            "End": f"{START_END_PATH}end.png",
            "Normal Zone": self.normal,
            "Blocked Zone": self.blocked,
            "Priority Zone": self.priority,
            "Restricted Zone": self.restricted,
        }

        legend_x = WINDOW_WIDTH - 375
        legend_y = 140

        for name, sprite in legend_sprite.items():
            if count == 4:
                legend_x = WINDOW_WIDTH - 200
                legend_y = 140

            icon = Icon(sprite, 0.175, name)

            icon.center_x = legend_x
            icon.center_y = legend_y
            icon.legend_label.x = legend_x + 30
            icon.legend_label.y = legend_y - 5

            self.legend_list.append(icon)

            legend_y -= 50

            count += 1

        # Builds the zones and their connections

        for zone, data in self.monitor.zones.items():
            x: float = (WINDOW_WIDTH / 2) + (
                data.x - self.center_gx
            ) * self.spacing
            y: float = (WINDOW_HEIGHT / 2) + (
                data.y - self.center_gy
            ) * self.spacing

            if zone == "start":
                self.start.center_x = x
                self.start.center_y = y + 35
                self.zone_list.append(self.start)

                text = OutlinedText(
                    text=data.name,
                    x=x,
                    y=y - 60,
                    color=Color.get_color(data.color),
                    outline_color=arcade.color.WHITE,
                    font_size=13,
                    anchor_x="center",
                    font_name="Minecraft",
                )
                self.text_list.append(text)

                self._create_drones(x, y)

            elif zone == "end":
                self.end.center_x = x
                self.end.center_y = y + 10
                self.zone_list.append(self.end)

                text = OutlinedText(
                    text=data.name,
                    x=x,
                    y=y - 90,
                    color=Color.get_color(data.color),
                    outline_color=arcade.color.WHITE,
                    font_size=13,
                    anchor_x="center",
                    font_name="Minecraft",
                )
                self.text_list.append(text)

            else:
                self._build_zone(data.name, data.zone, data.color, x, y)

        self._build_connections()

    def on_draw(self) -> None:
        """
        Renders the screen.
        """
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background,
                                 arcade.LBWH(0, 0,
                                             WINDOW_WIDTH,
                                             WINDOW_HEIGHT))

        # Draws a rectangle for the legend
        arcade.draw_rect_filled(arcade.rect.XYWH(WINDOW_WIDTH,
                                                 0,
                                                 WINDOW_WIDTH - 475,
                                                 WINDOW_HEIGHT - 565),
                                arcade.color.BEAVER)

        # Draws the selected map and the legend
        self.connection_list.draw()
        self.zone_list.draw()

        for icon in self.legend_list:
            icon.draw_text()

        # Draws the drones
        self.drone_list.draw()

        # Prints the zone and level name in the window
        for text in self.text_list:
            text.draw()

        self.legend_list.draw()
        self.turn_text.draw()


    def on_update(self, delta_time: float) -> None:
        """
        Advances the simulation and animates the drones.

        Parameters:
        - delta_time: float
        """
        if self._is_sim_started and not self._is_moving:
            self.monitor.simulate()
            self._start_drone_movement()

        if self._is_moving:
            self._move_drones(delta_time)

        self.turn_text.text = f"Turn {self.monitor.turn}"

        # Shows the number of turn at the end of the simulation
        # and stops it after 3 seconds
        if self.monitor.is_over() is True and not self._is_moving:
            print(self.monitor.summary())
            time.sleep(3)
            arcade.exit()

    def start_visual(self) -> None:
        """
        Starts the arcade visual.
        """
        arcade.run()

    def on_key_press(self, key: int, _modifiers: int) -> None:
        """
        Keyboard control.

        Parameters:
          - key: int
          - _modifiers: int
        """
        if key == arcade.key.ESCAPE:
            print("Closing the visual!")
            arcade.exit()

        if key == arcade.key.SPACE and self._is_sim_started is not True:
            print("Starting simulation")
            self._is_sim_started = True

    def _build_zone(
        self, name: str, zone: str, color: str, x: float, y: float
    ) -> None:
        """
        Builds the different zones and display their name below.

        Parameters:
          - name: str
          - zone: str
          - color: str
          - x: float
          - y: float
        """
        if zone == "normal":
            normal: arcade.Sprite = arcade.Sprite(
                self.normal, scale=self.sprite_scale
            )
            normal.center_x = x
            normal.center_y = y + 10

            self.zone_list.append(normal)

            text = OutlinedText(
                text=name,
                x=x,
                y=y - 65,
                color=Color.get_color(color),
                outline_color=arcade.color.WHITE,
                font_size=13,
                anchor_x="center",
                font_name="Minecraft",
            )
            self.text_list.append(text)

        if zone == "priority":
            priority: arcade.Sprite = arcade.Sprite(
                self.priority, scale=self.sprite_scale
            )
            priority.center_x = x
            priority.center_y = y + 20

            self.zone_list.append(priority)

            text = OutlinedText(
                text=name,
                x=x,
                y=y - 55,
                color=Color.get_color(color),
                outline_color=arcade.color.WHITE,
                font_size=13,
                anchor_x="center",
                font_name="Minecraft",
            )
            self.text_list.append(text)

        if zone == "restricted":
            restricted: arcade.Sprite = arcade.Sprite(
                self.restricted, scale=(self.sprite_scale * 0.75)
            )
            restricted.center_x = x
            restricted.center_y = y + 10

            self.zone_list.append(restricted)

            text = OutlinedText(
                text=name,
                x=x,
                y=y - 100,
                color=Color.get_color(color),
                outline_color=arcade.color.WHITE,
                font_size=13,
                anchor_x="center",
                font_name="Minecraft",
            )
            self.text_list.append(text)

        if zone == "blocked":
            blocked: arcade.Sprite = arcade.Sprite(
                self.blocked, scale=(self.sprite_scale * 0.75)
            )
            blocked.center_x = x
            blocked.center_y = y + 10

            self.zone_list.append(blocked)

            text = OutlinedText(
                text=name,
                x=x,
                y=y - 90,
                color=Color.get_color(color),
                outline_color=arcade.color.WHITE,
                font_size=13,
                anchor_x="center",
                font_name="Minecraft",
            )
            self.text_list.append(text)

    def _build_connections(self) -> None:
        """
        Builds the different connections between the zones.
        """
        from_p: tuple[int, int]
        to_p: tuple[int, int]

        from_x: float
        from_y: float
        to_x: float
        to_y: float

        for connection in self.monitor.visual_connections:
            from_p, to_p = connection

            from_x, from_y = from_p
            to_x, to_y = to_p

            from_x = (WINDOW_WIDTH / 2) + (
                from_x - self.center_gx
            ) * self.spacing
            from_y = (WINDOW_HEIGHT / 2) + (
                from_y - self.center_gy
            ) * self.spacing
            to_x = (WINDOW_WIDTH / 2) + (to_x - self.center_gx) * self.spacing
            to_y = (WINDOW_HEIGHT / 2) + (to_y - self.center_gy) * self.spacing

            line = arcade.shape_list.create_line(
                from_x, from_y, to_x, to_y, arcade.color.WHITE, 2
            )
            self.connection_list.append(line)

    def _create_drones(self, x: float, y: float) -> None:
        """
        Makes the drones on the start.

        Parameters:
          - x: float
          - y: float
        """
        self.drone_sprites: dict[str, arcade.Sprite] = {}

        for drone_name, drone_obj in self.monitor.drones.items():
            drone: arcade.Sprite = arcade.Sprite(
                self.drone, scale=(self.sprite_scale * 0.15)
            )
            drone.center_x = x - random.randint(0, 10)
            drone.center_y = y + random.randint(0, 10)

            self.drone_list.append(drone)
            self.drone_sprites[drone_name] = drone

    def _load_sprites(self) -> None:
        """
        Loads the necessary sprites.
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background image
            self.background: arcade.Texture = \
                arcade.load_texture(f"{BACK_PATH}back.png")

            # Creation of the different types of hubs
            self.start: arcade.Sprite = arcade.Sprite(
                f"{START_END_PATH}start.png", scale=self.sprite_scale
            )
            self.end: arcade.Sprite = arcade.Sprite(
                f"{START_END_PATH}end.png", scale=self.sprite_scale
            )

            self.normal: arcade.Texture = arcade.load_texture(
                f"{HUB_PATH}normal.png"
            )
            self.priority: arcade.Texture = arcade.load_texture(
                f"{HUB_PATH}priority.png"
            )
            self.restricted: arcade.Texture = arcade.load_texture(
                f"{HUB_PATH}restricted.png"
            )
            self.blocked: arcade.Texture = arcade.load_texture(
                f"{HUB_PATH}blocked.png"
            )

            # Creation of a drone
            self.drone = arcade.load_texture(f"{DRONE_PATH}bee.png")

        except FileNotFoundError:
            raise ValueError("Assets folder not found")

    def _start_drone_movement(self) -> None:
        """
        Sets the pixel target of every drone sprite based on
        the zone the drone is now heading to.
        """
        any_moving: bool = False

        for drone_name, drone_obj in self.monitor.drones.items():
            if drone_obj.has_finished:
                continue

            sprite = self.drone_sprites.get(drone_name)
            if sprite is None:
                continue

            target_name = drone_obj.get_position()
            if target_name is None:
                continue

            target_zone = self.monitor.zones.get(target_name)
            if target_zone is None:
                continue

            target_x: float = (WINDOW_WIDTH / 2) + (
                target_zone.x - self.center_gx
            ) * self.spacing
            target_y: float = (WINDOW_HEIGHT / 2) + (
                target_zone.y - self.center_gy
            ) * self.spacing

            sprite.target_x = target_x
            sprite.target_y = target_y

            any_moving = True

        self._is_moving = any_moving

    def _move_drones(self, delta_time: float) -> None:
        """
        Moves every drone sprite toward its target position.

        Parameters:
        - delta_time: float
        """
        still_moving: bool = False

        for sprite in self.drone_sprites.values():
            target_x = getattr(sprite, "target_x", sprite.center_x)
            target_y = getattr(sprite, "target_y", sprite.center_y)

            dx = target_x - sprite.center_x
            dy = target_y - sprite.center_y
            distance = math.hypot(dx, dy)

            if distance < 2:
                sprite.center_x = target_x
                sprite.center_y = target_y
                continue

            still_moving = True
            step = DRONE_SPEED * delta_time

            if step >= distance:
                sprite.center_x = target_x
                sprite.center_y = target_y
            else:
                sprite.center_x += dx / distance * step
                sprite.center_y += dy / distance * step

        self._is_moving = still_moving
