import os
import arcade

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

SCALE = 0.5
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
    def __init__(self, monitor: Monitor) -> None:
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                         title=TITLE, resizable=True,
                         center_window=True)

        self.background_color = arcade.color.BLUE_BELL
        self.monitor = monitor

        self._load_sprites()
        self._setup()

    def _setup(self) -> None:
        """
        Initialize the visual.

        Return
            -> None
        """
        self.zone_list: arcade.SpriteList = arcade.SpriteList()

        for zone, data in self.monitor.zones.items():
            if zone == "start":
                self.start.center_x = data.x
                self.start.center_y = data.y
                self.zone_list.append(self.start)

            elif zone == "end":
                self.end.center_x = data.x
                self.end.center_y = data.y
                self.zone_list.append(self.end)

            else:
                if data.zone == "normal":
                    self.normal.center_x = data.x
                    self.normal.center_y = data.y
                    self.zone_list.append(self.normal)

                if data.zone == "priority":
                    self.priority.center_x = data.x
                    self.priority.center_y = data.y
                    self.zone_list.append(self.priority)

                if data.zone == "restricted":
                    self.restricted.center_x = data.x
                    self.restricted.center_y = data.y
                    self.zone_list.append(self.restricted)

                if data.zone == "blocked":
                    self.blocked.center_x = data.x
                    self.blocked.center_y = data.y
                    self.zone_list.append(self.blocked)

    def on_draw(self) -> None:
        """
        Renders the screen.

        Return
            -> None
        """
        self.clear()

        # arcade.draw_texture_rect(self.background,
        #                          arcade.LBWH(0, 0, self.width, self.height))

        self.zone_list.draw()

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

        Return
            -> None
        """
        if key == arcade.key.ESCAPE:
            print("Closing the visual!")
            arcade.exit()

    def _build_zone(self) -> None:
        pass

    def _load_sprites(self) -> None:
        """
        Loads the necessary sprites.

        Return
            -> None
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # self.background: arcade.Texture = \
            #     arcade.Texture(f"{BACK_PATH}")

            # Creation of the different types of hubs
            self.start: arcade.Sprite = \
                arcade.Sprite(f"{START_END_PATH}start.png",
                              scale=SCALE)
            self.end: arcade.Sprite = arcade.Sprite(f"{START_END_PATH}end.png",
                                                    scale=SCALE)

            self.normal: arcade.Sprite = arcade.Sprite(f"{HUB_PATH}normal.png")
            self.priority: arcade.Sprite = \
                arcade.Sprite(f"{HUB_PATH}priority.png")
            self.restricted: arcade.Sprite = \
                arcade.Sprite(f"{HUB_PATH}restricted.png")
            self.blocked: arcade.Sprite = \
                arcade.Sprite(f"{HUB_PATH}blocked.png")

            # Creation of a drone
            # self.drone = arcade.Sprite(f"{DRONE_PATH}bee.gif")

        except FileNotFoundError:
            raise ValueError("Assets folder not found")
