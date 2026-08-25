import os
import arcade

from typing import Any

from src.monitor import Monitor

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
OFFSET = WINDOW_WIDTH / 3.5
# ----------------- #


class Visualizer(arcade.Window):
    """
    This class will create a window in which
    there will be a visual of the map.

    Attributes:
      - on_draw(self) -> None
      - start(self) -> None
      - on_key_press(self, key: int, _modifiers: int) -> None
      - _load_sprites(self) -> None
    """
    def __init__(self, lvl_name: str, monitor: Monitor) -> None:
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                         title=TITLE, resizable=True,
                         center_window=True)

        self.background_color = arcade.color.BLUE_BELL

        self.lvl_name = lvl_name
        self.monitor = monitor

        self._load_sprites()
        self._setup()
        self._build_connections()

    def _setup(self) -> None:
        """
        Initializes the visual.

        Return
            -> None
        """
        self.zone_list: arcade.SpriteList = arcade.SpriteList()
        self.connection_list: (arcade.shape_list.
                               ShapeElementList[arcade.shape_list.Shape]) = \
                                arcade.shape_list.ShapeElementList()
        self.text_list: list[arcade.Text] = []

        text = arcade.Text(text=self.lvl_name,
                           x=1300 / 2, y=850,
                           color=arcade.color.WHITE,
                           font_size=25, anchor_x="center",
                           font_name="Minecraft")
        self.text_list.append(text)

        for zone, data in self.monitor.zones.items():
            x: int = ((WINDOW_WIDTH / 2) + (data.x * SPRITE_SIZE) - OFFSET)
            y: int = ((WINDOW_HEIGHT / 2) + (data.y * SPRITE_SIZE))

            if zone == "start":
                self.start.center_x = x
                self.start.center_y = y
                self.zone_list.append(self.start)

                text = arcade.Text(text=data.name,
                                   x=x, y=y - 100,
                                   color=arcade.color.WHITE,
                                   font_size=13, anchor_x="center",
                                   font_name="Minecraft")
                self.text_list.append(text)

            elif zone == "end":
                self.end.center_x = x
                self.end.center_y = y
                self.zone_list.append(self.end)

                text = arcade.Text(text=data.name,
                                   x=x, y=y - 100,
                                   color=arcade.color.WHITE,
                                   font_size=13, anchor_x="center",
                                   font_name="Minecraft")
                self.text_list.append(text)

            else:
                self._build_zone(data.name, data.zone, x, y)

    def on_draw(self) -> None:
        """
        Renders the screen.

        Return
            -> None
        """
        self.clear()

        # arcade.draw_texture_rect(self.background,
        #                          arcade.LBWH(0, 0, self.width, self.height))

        # Draws the selected map
        self.connection_list.draw()
        self.zone_list.draw()

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

    def _build_zone(self, name: str, zone: str, x: int, y: int) -> None:
        """
        Builds the different zones and display their name below.

        Parameters:
          - name: str
          - zone: str
          - x: int
          - y: int

        Return
            -> None
        """
        if zone == "normal":
            normal: arcade.Sprite = arcade.Sprite(self.normal,
                                                  scale=SCALE)
            normal.center_x = x
            normal.center_y = y

            self.zone_list.append(normal)

            text = arcade.Text(text=name,
                               x=x, y=y - 75,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "priority":
            priority: arcade.Sprite = arcade.Sprite(self.priority,
                                                    scale=SCALE)
            priority.center_x = x
            priority.center_y = y

            self.zone_list.append(priority)

            text = arcade.Text(text=name,
                               x=x, y=y - 75,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "restricted":
            restricted: arcade.Sprite = arcade.Sprite(self.restricted,
                                                      scale=SCALE)
            restricted.center_x = x
            restricted.center_y = y

            self.zone_list.append(restricted)

            text = arcade.Text(text=name,
                               x=x, y=y - 125,
                               color=arcade.color.WHITE,
                               font_size=13, anchor_x="center",
                               font_name="Minecraft")
            self.text_list.append(text)

        if zone == "blocked":
            blocked: arcade.Sprite = arcade.Sprite(self.blocked,
                                                   scale=SCALE)
            blocked.center_x = x
            blocked.center_y = y

            self.zone_list.append(blocked)

            text = arcade.Text(text=name,
                               x=x, y=y - 100,
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
        from_p: tuple[int, int] = ()
        to_p: tuple[int, int] = ()

        from_x: int
        from_y: int
        to_x: int
        to_y: int

        for connection in self.monitor.visual_connections:
            from_p, to_p = connection

            from_x, from_y = from_p
            to_x, to_y = to_p

            line = arcade.shape_list.create_line(from_x, from_y,
                                                 to_x, to_y,
                                                 arcade.color.BLACK,
                                                 3)
            self.connection_list.append(line)

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
            #     arcade.load_texture(f"{BACK_PATH}")

            # Creation of the different types of hubs
            self.start: arcade.Sprite = \
                arcade.Sprite(f"{START_END_PATH}start.png",
                              scale=SCALE)
            self.end: arcade.Sprite = arcade.Sprite(f"{START_END_PATH}end.png",
                                                    scale=SCALE)

            self.normal: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}normal.png")
            self.priority: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}priority.png")
            self.restricted: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}restricted.png")
            self.blocked: arcade.Texture = \
                arcade.load_texture(f"{HUB_PATH}blocked.png")

            # Creation of a drone
            # self.drone = arcade.Sprite(f"{DRONE_PATH}bee.gif")

            # Loads the text font
            arcade.load_font(f"{FONT_PATH}MinecraftFont.woff")

        except FileNotFoundError:
            raise ValueError("Assets folder not found")
