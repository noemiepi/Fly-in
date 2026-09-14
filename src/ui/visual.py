import os
import arcade
import random

from src.monitor import Monitor
from src.ui.utils.icon import Icon

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
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                         title=TITLE, resizable=True,
                         center_window=True)

        self.background_color = arcade.color.BLUE_BELL

        self.lvl_name = lvl_name
        self.monitor = monitor

        self.setup()

    def setup(self) -> None:
        """
        Initializes the visual.

        Return
            -> None
        """
        self.zone_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.drone_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.connection_list: (arcade.shape_list.
                               ShapeElementList[arcade.shape_list.Shape]) = \
            arcade.shape_list.ShapeElementList()

        self.legend_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.text_list: list[arcade.Text] = []

        # Loads the text font
        arcade.load_font(f"{FONT_PATH}MinecraftFont.woff")

        text = arcade.Text(text=self.lvl_name,
                           x=1300 / 2, y=850,
                           color=arcade.color.WHITE,
                           font_size=25, anchor_x="center",
                           font_name="Minecraft")
        self.text_list.append(text)

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
        legend_sprite: dict[str, arcade.Sprite] = {
            "Start": f"{START_END_PATH}start.png",
            "End": f"{START_END_PATH}end.png",
            "Normal Zone": self.normal,
            "Blocked Zone": self.blocked,
            "Priority Zone": self.priority,
            "Restricted Zone": self.restricted
            }

        legend_x = WINDOW_WIDTH - 200
        legend_y = 300

        for name, sprite in legend_sprite.items():
            icon = Icon(sprite, 0.2, name)

            icon.center_x = legend_x
            icon.center_y = legend_y
            icon.legend_label.x = legend_x + 15
            icon.legend_label.y = legend_y - 5

            self.legend_list.append(icon)

            legend_y -= 50

        for zone, data in self.monitor.zones.items():
            x: float = ((WINDOW_WIDTH / 2) + (data.x - self.center_gx)
                        * self.spacing)
            y: float = ((WINDOW_HEIGHT / 2) + (data.y - self.center_gy)
                        * self.spacing)

            if zone == "start":
                self.start.center_x = x
                self.start.center_y = y + 35
                self.zone_list.append(self.start)

                text = arcade.Text(text=data.name,
                                   x=x, y=y - 60,
                                   color=arcade.color.WHITE,
                                   font_size=13, anchor_x="center",
                                   font_name="Minecraft")
                self.text_list.append(text)

                self._create_drones(x, y)

            elif zone == "end":
                self.end.center_x = x
                self.end.center_y = y + 10
                self.zone_list.append(self.end)

                text = arcade.Text(text=data.name,
                                   x=x, y=y - 90,
                                   color=arcade.color.WHITE,
                                   font_size=13, anchor_x="center",
                                   font_name="Minecraft")
                self.text_list.append(text)

            else:
                self._build_zone(data.name, data.zone, x, y)

        self._build_connections()

    def on_draw(self) -> None:
        """
        Renders the screen.

        Return
            -> None
        """
        self.clear()

        # Draws the background
        # arcade.draw_texture_rect(self.background,
        #                          arcade.LBWH(0, 0,
        #                                      WINDOW_WIDTH,
        #                                      WINDOW_HEIGHT))

        # Draws the selected map and the legend
        self.connection_list.draw()
        self.zone_list.draw()
        self.legend_list.draw()

        for sprite in self.legend_list:
            sprite

        # Draws the drones
        self.drone_list.draw()

        # Prints the zone and level name in the window
        for text in self.text_list:
            text.draw()

    def start_visual(self) -> None:
        """
        Starts the arcade visual.

        Return
            -> None
        """
        arcade.run()

    def on_key_press(self, key: int, _modifiers: int) -> None:
        """
        Keyboard control.

        Parameters:
          - key: int
          - _modifiers: int

        Return
            -> None
        """
        if key == arcade.key.ESCAPE:
            print("Closing the visual!")
            arcade.exit()

    def _build_zone(self, name: str, zone: str, x: float, y: float) -> None:
        """
        Builds the different zones and display their name below.

        Parameters:
          - name: str
          - zone: str
          - x: float
          - y: float

        Return
            -> None
        """
        if zone == "normal":
            normal: arcade.Sprite = arcade.Sprite(self.normal,
                                                  scale=self.sprite_scale)
            normal.center_x = x
            normal.center_y = y + 10

            self.zone_list.append(normal)

            text = arcade.Text(text=name,
                               x=x, y=y - 65,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "priority":
            priority: arcade.Sprite = arcade.Sprite(self.priority,
                                                    scale=self.sprite_scale)
            priority.center_x = x
            priority.center_y = y + 20

            self.zone_list.append(priority)

            text = arcade.Text(text=name,
                               x=x, y=y - 55,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "restricted":
            restricted: arcade.Sprite = arcade.Sprite(self.restricted,
                                                      scale=(self.sprite_scale
                                                             * 0.75))
            restricted.center_x = x
            restricted.center_y = y + 10

            self.zone_list.append(restricted)

            text = arcade.Text(text=name,
                               x=x, y=y - 100,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "blocked":
            blocked: arcade.Sprite = arcade.Sprite(self.blocked,
                                                   scale=(self.sprite_scale
                                                          * 0.75))
            blocked.center_x = x
            blocked.center_y = y + 10

            self.zone_list.append(blocked)

            text = arcade.Text(text=name,
                               x=x, y=y - 90,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

    def _build_connections(self) -> None:
        """
        Builds the different connections between the zones.

        Return
            -> None
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

            from_x = ((WINDOW_WIDTH / 2) + (from_x - self.center_gx)
                      * self.spacing)
            from_y = ((WINDOW_HEIGHT / 2) + (from_y - self.center_gy)
                      * self.spacing)
            to_x = ((WINDOW_WIDTH / 2) + (to_x - self.center_gx)
                    * self.spacing)
            to_y = ((WINDOW_HEIGHT / 2) + (to_y - self.center_gy)
                    * self.spacing)

            line = arcade.shape_list.create_line(from_x, from_y,
                                                 to_x, to_y,
                                                 arcade.color.WHITE, 2)
            self.connection_list.append(line)

    def _create_drones(self, x: float, y: float) -> None:
        """
        Makes the drones on the start.

        Parameters:
          - x: float
          - y: float

        Return
            -> None
        """

        for drones in self.monitor.drones:
            drone: arcade.Sprite = arcade.Sprite(self.drone,
                                                 scale=(self.sprite_scale
                                                        * 0.15))
            drone.center_x = x - random.randint(0, 10)
            drone.center_y = y + random.randint(0, 10)

            self.drone_list.append(drone)

    def _load_sprites(self) -> None:
        """
        Loads the necessary sprites.

        Return
            -> None
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background image
            # self.background: arcade.Texture = \
            #     arcade.load_texture(f"{BACK_PATH}back.png")

            # Creation of the different types of hubs
            self.start: arcade.Sprite = \
                arcade.Sprite(f"{START_END_PATH}start.png",
                              scale=self.sprite_scale)
            self.end: arcade.Sprite = arcade.Sprite(f"{START_END_PATH}end.png",
                                                    scale=self.sprite_scale)

            self.normal: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}normal.png")
            self.priority: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}priority.png")
            self.restricted: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}restricted.png")
            self.blocked: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}blocked.png")

            # Creation of a drone
            self.drone = arcade.load_texture(f"{DRONE_PATH}bee.png")

        except FileNotFoundError:
            raise ValueError("Assets folder not found")
