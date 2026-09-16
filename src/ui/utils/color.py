from src.ui.utils.x11_colors import X11_NAMES


class Color():
    def get_color(color_name: str) -> tuple[int, int, int]:
        name = color_name.lower()

        if name not in X11_NAMES:
            return (255, 255, 255)

        for color, code in X11_NAMES.items():
            if name == color:
                hex_code: str = code.strip("#")
                break

        r: int = int(hex_code[0:2], 16)
        g: int = int(hex_code[2:4], 16)
        b: int = int(hex_code[4:6], 16)

        return (r, g, b)
