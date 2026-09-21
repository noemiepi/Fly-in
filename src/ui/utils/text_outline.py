import arcade


class OutlinedText:
    """
    A class to draw an outline to a text.
    """
    _DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),            (0, 1),
        (1, -1),   (1, 0),  (1, 1),
    ]

    def __init__(
            self,
            text: str,
            x: float,
            y: float,
            color: arcade.types.Color,
            font_size: float,
            outline_color: arcade.types.Color = arcade.color.BLACK,
            thickness: int = 2,
            **kwargs
    ) -> None:
        self.outlines: list[arcade.Text] = [
            arcade.Text(
                text=text,
                x=x + dx * thickness,
                y=y + dy * thickness,
                color=outline_color,
                font_size=font_size,
                **kwargs
            )
            for dx, dy in self._DIRECTIONS
        ]
        self.main = arcade.Text(
            text=text, x=x, y=y, color=color, font_size=font_size, **kwargs
        )

    @property
    def text(self) -> str:
        return self.main.text

    @text.setter
    def text(self, value: str) -> None:
        self.main.text = value
        for outline in self.outlines:
            outline.text = value

    def draw(self) -> None:
        for outline in self.outlines:
            outline.draw()
        self.main.draw()
