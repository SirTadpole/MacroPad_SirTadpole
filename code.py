"""
A fairly straightforward macro/hotkey program for Adafruit MACROPAD.
Macro key setups are stored in the /macros folder (configurable below),
load up just the ones you're likely to use. Plug into computer's USB port,
use dial to select an application macro set, press MACROPAD keys to send
key sequences.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import displayio
import terminalio
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad


# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'


# CLASSES AND FUNCTIONS ----------------

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros):  # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.pixels.show()
        macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

macropad.display_image("intro.bmp")
time.sleep(2)

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(
        label.Label(
            terminalio.FONT,
            text='',
            color=0xFFFFFF,
            anchored_position=(
                (macropad.display.width - 1) * x / 2,
                macropad.display.height - 1 - (3 - y) * 12),
            anchor_point=(x / 2, 1.0)
        )
    )
group.append(
    Rect(
        0,
        0,
        macropad.display.width,
        12,
        fill=0xFFFFFF
    )
)
group.append(
    label.Label(
        terminalio.FONT,
        text='',
        color=0x000000,
        anchored_position=(macropad.display.width//2, -2),
        anchor_point=(0.5, 0.0)
    )
)
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            pass

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

clickSwitch = 0
position = 0
last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    # position = macropad.encoder
    # if position != last_position:
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        print("Switch Macro App")
        clickSwitch = clickSwitch + 1
        app_index = clickSwitch % len(apps)
        apps[app_index].switch()
    else:
        last_position = position
        position = macropad.encoder

        if last_position > position:
            print("----->")
            macropad.display.refresh()
            macropad.keyboard.press(Keycode.LEFT_ARROW)
            macropad.keyboard.release(Keycode.LEFT_ARROW)
        elif last_position < position:
            print("<-----")
            macropad.display.refresh()
            macropad.keyboard.press(Keycode.RIGHT_ARROW)
            macropad.keyboard.release(Keycode.RIGHT_ARROW)

        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue  # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

        sequence = apps[app_index].macros[key_number][2]
        if pressed:
            if key_number < 12:  # No pixel for encoder button
                macropad.pixels[key_number] = 0xFFFFFF
                macropad.pixels.show()
            for item in sequence:
                if isinstance(item, int):
                    if item >= 0:
                        macropad.keyboard.press(item)
                    else:
                        macropad.keyboard.release(-item)
                else:
                    macropad.keyboard_layout.write(item)
        else:
            # Release any still-pressed modifier keys
            for item in sequence:
                if isinstance(item, int) and item >= 0:
                    macropad.keyboard.release(item)
            if key_number < 12:  # No pixel for encoder button
                macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
                macropad.pixels.show()

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.