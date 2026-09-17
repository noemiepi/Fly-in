import arcade

from arcade.types import PathOrTexture


class Icon(arcade.Sprite):
    """
    Gives a visual representation of the legend.
    """
    def __init__(self, path: PathOrTexture, scale: float, name: str) -> None:
        super().__init__(path, scale)

        self.legend_label = arcade.Text(text=name, x=0, y=0,
                                        anchor_x="left", anchor_y="center",
                                        color=arcade.color.WHITE,
                                        font_size=12,
                                        font_name="Minecraft")

    def draw_text(self) -> None:
        """
        A method to draw the text of the icon.
        """
        self.legend_label.draw()
