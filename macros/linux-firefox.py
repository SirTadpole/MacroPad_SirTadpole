# MACROPAD Hotkeys example: Firefox web browser for Linux

# a600ff - Violet
# ff0000 - Red
# ff9900 - Orange
# 000040 - Blue
# 101010 - Black/White

from adafruit_hid.keycode import Keycode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Linux Firefox',
    'macros' : [
    # 1st row ----------
        # COLOR    LABEL        KEY SEQUENCE
        (0x000040, '< Prev',    [Keycode.ALT, Keycode.LEFT_ARROW]),
        (0x000040, 'Next >',    [Keycode.ALT, Keycode.RIGHT_ARROW]),
        (0xa600ff, 'Up',        [Keycode.SHIFT, ' ']),
        # 2nd row ----------
        # COLOR    LABEL        KEY SEQUENCE
        (0xff9900, '< Tab',     [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        (0xff9900, 'Tab >',     [Keycode.CONTROL, Keycode.TAB]),
        (0xa600ff, 'Down',      ' '),
        # 3rd row ----------
        # COLOR    LABEL        KEY SEQUENCE
        (0x101010, 'Reload',    [Keycode.CONTROL, 'r']),
        (0x101010, 'Home',      [Keycode.CONTROL, 'h']),
        (0x101010, 'Private',   [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        # 4th row ----------
        # COLOR    LABEL        KEY SEQUENCE
        (0x101010, 'Google',    [Keycode.CONTROL, 't', -Keycode.CONTROL,
                                'zzz<google<fr\n']),
        (0xff0000, 'Dev',       [Keycode.F12]),
        (0x101010, 'Mail',      [Keycode.CONTROL, 't', -Keycode.CONTROL,
                                'zzz<;qil<google<fr\n'])
    ]
}