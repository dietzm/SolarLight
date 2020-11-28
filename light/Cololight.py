import socket

class PyCololight:
    COMMAND_PREFIX = "535a30300000000000"
    COMMAND_CONFIG = "20000000000000000000000000000000000100000000000000000004010301c"
    COMMAND_EFFECT = "23000000000000000000000000000000000100000000000000000004010602ff"
    CUSTOM_EFFECT_COLOURS = {
        "Breath": {
            "decimal": 128,
            "colours": (
                "Red, Green, Blue",
                "Rainbow",
                "Green",
                "Azure",
                "Blue",
                "Purple",
                "Red",
                "Orange",
                "Yellow",
                "White",
                "Green, Blue",
            ),
        },
        "Shadow": {
            "decimal": 139,
            "colours": (
                "Red, Yellow",
                "Red, Green",
                "Red, Blue",
                "Green, Yellow",
                "Green, Azure",
                "Green, Blue",
                "Blue, Azure",
                "Blue, Purple",
                "Yellow, White",
                "Red, White",
                "Green, White",
                "Azure, White",
                "Blue, White",
                "Purple, White",
            ),
        },
        "Flash": {
            "decimal": 153,
            "colours": (
                "Red, Green, Blue",
                "Rainbow",
                "Green",
                "Azure",
                "Blue",
                "Purple",
                "Red",
                "Orange",
                "Yellow",
                "White",
            ),
        },
        "Flicker": {
            "decimal": 163,
            "colours": (
                "Red, Green, Blue",
                "Rainbow",
                "Green",
                "Azure",
                "Blue",
                "Purple",
                "Red",
                "Orange",
                "Yellow",
                "White",
            ),
        },
        "Scene": {
            "decimal": 173,
            "colours": (
                "Birthday",
                "Girlfriends",
                "Friends",
                "Workmates",
                "Family",
                "Lover",
            ),
        },
        "Mood": {
            "decimal": 179,
            "colours": (
                "Red",
                "Orange",
                "Yellow",
                "Green",
                "Grass",
                "Azure",
                "Blue",
                "Pink",
                "Gold",
                "Color",
                "True Color",
            ),
        },
        "Selected": {
            "decimal": 191,
            "colours": ("Savasana", "", "Sunrise", "", "Unicorns"),
        },
    }
    CUSTOM_EFFECT_MODES = [
        ("01", "00"),
        ("02", "00"),
        ("05", "10"),
        ("05", "30"),
        ("05", "40"),
        ("05", "50"),
        ("05", "70"),
        ("05", "80"),
        ("05", "90"),
        ("05", "a0"),
        ("05", "b0"),
        ("05", "c0"),
        ("05", "00"),
        ("05", "20"),
        ("05", "30"),
        ("06", "00"),
        ("06", "10"),
        ("06", "20"),
        ("06", "30"),
        ("06", "50"),
        ("05", "f0"),
        ("05", "10"),
        ("05", "40"),
        ("05", "50"),
        ("06", "60"),
        ("06", "70"),
        ("06", "80"),
    ]

    def __init__(self, host, port=8900):
        self.host = host
        self.port = port
        self._on = False
        self._brightness = None
        self._colour = None
        self._effect = None
        self._effects = {
            "80s Club": "049a0000",
            "Cherry Blossom": "04940800",
            "Cocktail Parade": "05bd0690",
            "Instagrammer": "03bc0190",
            "Pensieve": "04c40600",
            "Savasana": "04970400",
            "Sunrise": "01c10a00",
            "The Circus": "04810130",
            "Unicorns": "049a0e00",
            "Christmas": "068b0900",
            "Rainbow Flow": "03810690",
            "Music Mode": "07bd0990",
        }
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _send(self, command):
        self._sock.sendto(command, (self.host, self.port))

    def _cycle_speed_hex(self, cycle_speed, mode):
        if not 1 <= cycle_speed <= 32:
            raise CycleSpeedException
        if mode in [2]:
            # Mode 2 only has speeds 1, 2, 3, which are mapped differently to other modes
            cycle_speed_values = [3, 11, 19]
            cycle_speed_value = cycle_speed_values[min(3, cycle_speed) - 1]
        else:
            cycle_speed_value = list(reversed(range(33)))[cycle_speed - 1]

        cycle_speed_hex = "{:02x}".format(cycle_speed_value)
        return cycle_speed_hex

    def _colour_hex(self, colour_scheme, colour, mode):
        if colour_scheme not in self.custom_effect_colour_schemes():
            raise ColourSchemeException
        if colour not in self.custom_effect_colour_scheme_colours(colour_scheme):
            raise ColourException

        starting_decimal = self.CUSTOM_EFFECT_COLOURS[colour_scheme]["decimal"]
        colour_key = self.CUSTOM_EFFECT_COLOURS[colour_scheme]["colours"].index(colour)
        if mode in [13, 14, 15, 22, 23, 24]:
            # These modes have a lower starting decimal of 128
            starting_decimal = starting_decimal - 128
        colour_decimal = starting_decimal + colour_key
        colour_hex = "{:02x}".format(colour_decimal)
        return colour_hex

    def _mode_hex(self, mode):
        if not 1 <= mode <= len(self.CUSTOM_EFFECT_MODES):
            raise ModeExecption

        return self.CUSTOM_EFFECT_MODES[mode - 1]

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, brightness):
        if brightness:
            self._on = True
            self.brightness = brightness
        else:
            self._on = False
            command = bytes.fromhex(
                "{}{}{}".format(self.COMMAND_PREFIX, self.COMMAND_CONFIG, "e1e")
            )
            self._send(command)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        brightness_prefix = "f"
        command = bytes.fromhex(
            "{}{}{}{:02x}".format(
                self.COMMAND_PREFIX,
                self.COMMAND_CONFIG,
                brightness_prefix,
                int(brightness),
            )
        )
        self._brightness = brightness
        self._send(command)

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        colour_prefix = "00"
        command = bytes.fromhex(
            "{}{}{}{:02x}{:02x}{:02x}".format(
                self.COMMAND_PREFIX, self.COMMAND_EFFECT, colour_prefix, *colour
            )
        )
        self._colour = colour
        self._send(command)

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, effect):
        command = bytes.fromhex(
            "{}{}{}".format(
                self.COMMAND_PREFIX,
                self.COMMAND_EFFECT,
                self._effects[effect],
            )
        )
        self._effect = effect
        self._send(command)

    @property
    def effects(self):
        return list(self._effects.keys())

    def add_custom_effect(self, name, colour_scheme, colour, cycle_speed, mode):
        cycle_speed_hex = self._cycle_speed_hex(int(cycle_speed), int(mode))
        colour_hex = self._colour_hex(colour_scheme, colour, int(mode))
        mode_hex = self._mode_hex(int(mode))

        if mode in [2]:
            # Mode 2 has bytes arranged differently to other modes
            custom_effect_hex = (
                f"{mode_hex[0]}{cycle_speed_hex}{colour_hex}{mode_hex[1]}"
            )
        else:
            custom_effect_hex = (
                f"{mode_hex[0]}{colour_hex}{cycle_speed_hex}{mode_hex[1]}"
            )

        self._effects[name] = custom_effect_hex

    def custom_effect_colour_schemes(self):
        return list(self.CUSTOM_EFFECT_COLOURS.keys())

    def custom_effect_colour_scheme_colours(self, colour_scheme):
        return list(filter(None, self.CUSTOM_EFFECT_COLOURS[colour_scheme]["colours"]))


class ColourSchemeException(Exception):
    pass


class ColourException(Exception):
    pass


class CycleSpeedException(Exception):
    pass


class ModeExecption(Exception):
    pass