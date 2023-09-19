"""This file contains most of the classes used in the program."""

# colorful print


class TextColors:
    """This class contains the colors of the text."""
    class TextStyle:
        """This class contains the styles of the text."""
        N = 0
        B = 1
        U = 4

    class Color:
        """This class contains the colors of the text."""
        BK = 30
        R = 31
        G = 32
        Y = 33
        BL = 34
        P = 35
        C = 36
        W = 37

    class BackgroundColor:
        """This class contains the colors of the background."""
        BK = 40
        R = 41
        G = 42
        Y = 43
        BL = 44
        P = 45
        C = 46
        W = 47

    C = "\x1b[0m"


class ColorfulText:
    """This class is used to print store colorful text."""

    def __init__(self,
                 text: str,
                 style: TextColors.TextStyle = TextColors.TextStyle.N,
                 color: TextColors.Color = TextColors.Color.W,
                 background_color: TextColors.BackgroundColor = TextColors.BackgroundColor.BK,
                 close: bool = True
                 ):
        self.text = text
        self.style = style
        self.color = color
        self.background_color = background_color
        self.close = close

    def __str__(self):
        return f"\x1b[{self.style};{self.color};{self.background_color}m{self.text}"+TextColors.C if self.close else f"\x1b[{self.style};{self.color};{self.background_color}m{self.text}"

    def __repr__(self):
        return f"\x1b[{self.style};{self.color};{self.background_color}m{self.text}"+TextColors.C if self.close else f"\x1b[{self.style};{self.color};{self.background_color}m{self.text}"

    def __add__(self, other: str):
        return self.text + other

    def __len__(self):
        return len(self.text)

    def __eq__(self, other):
        return self.text == other

    def __ne__(self, other):
        return self.text != other

    def __contains__(self, other):
        return other in self.text

    def __getitem__(self, key):
        return self.text[key]

    def __setitem__(self, key, value):
        self.text[key] = value

    def __delitem__(self, key):
        del self.text[key]

    def __iter__(self):
        return iter(self.text)

    def __reversed__(self):
        return reversed(self.text)

    def __copy__(self):
        return self.text.copy()

    def __deepcopy__(self, memo):
        return self.text.deepcopy(memo)

    def __hash__(self):
        return hash(self.text)

    def __bool__(self):
        return bool(self.text)

    def __format__(self, format_spec):
        return self.text.format(format_spec)

    def get_style(self):
        """Get the style of the text."""
        return self.style

    def get_color(self):
        """Get the color of the text."""
        return self.color

    def get_background_color(self):
        """Get the background color of the text."""
        return self.background_color


def colorful_print(text, level: str = "INFO", end: str = "\n"):
    """Print the text."""
    if level == "INFO":
        print(
            f"\x1b[;{TextColors.Color.BL};{TextColors.BackgroundColor.BK}m{text}"+TextColors.C, end=end
        )
    elif level == "WARNING":
        print(
            f"\x1b[;{TextColors.Color.Y};{TextColors.BackgroundColor.BK}m{text}"+TextColors.C, end=end
        )
    elif level == "ERROR":
        print(
            f"\x1b[;{TextColors.Color.R};{TextColors.BackgroundColor.BK}m{text}"+TextColors.C, end=end
        )
    elif level == "SUCCESS":
        print(
            f"\x1b[;{TextColors.Color.G};{TextColors.BackgroundColor.BK}m{text}"+TextColors.C, end=end
        )
    elif level == "PROCESSING":
        print(
            f"\x1b[;{TextColors.Color.P};{TextColors.BackgroundColor.BK}m{text}"+TextColors.C, end=end
        )
    else:
        print(text, end=end)
