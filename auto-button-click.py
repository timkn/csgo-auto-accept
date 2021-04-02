import cv2
import pyautogui
import numpy as np
from configparser import ConfigParser

import time
import sys
import json

config_refresh = 1
config_threshold = 0.7  # A threshold value of 0.6 is very "aggressive"
config_img_csgo_accept_button_paths = ["csgo-accept-bt-1.jpg"]  # default image path
config_click_duration = 0.2
config_show_img = False

START_TEXT = """
CS:GO Auto Accept - V 1.0 by tym.21
"""
EXIT_TEXT = "goodbye."

CONFIG_FILE_NAME = "config.ini"


# Created by Tim 2021
# GitHub: tym21

def load_config():
    global config_refresh
    global config_img_csgo_accept_button_paths
    global config_threshold
    global config_click_duration
    global config_show_img

    config = ConfigParser()
    try:
        config.read(CONFIG_FILE_NAME)
        config_refresh = int(config["DEFAULT"]["refresh"])
        config_img_csgo_accept_button_paths = json.loads(config.get("DEFAULT", "img_csgo_accept_button_path"))
        config_threshold = float(config["DEFAULT"]["threshold"])
        config_click_duration = float(config["DEFAULT"]["click_duration"])
        config_show_img = config["DEFAULT"].getboolean("show_img")
    except KeyError:
        print(
            'Config could not be loaded. The "config.ini" file must be in the same folder as the python file. '
            'All variables must be named exactly the same. Load a new config file from GitHub. '
            'The default config is now used, but the paths will not be correct.')

    print(f"Config loaded: {config_refresh=} {config_threshold=} {config_click_duration=} {config_show_img=} "
          f"{config_img_csgo_accept_button_paths=}")


def find_img_on_screen(image, template, template_name=""):
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(f"Template {template_name}: {max_val=}")
    if max_val >= config_threshold:
        return True, max_loc, max_val  # max_loc = top_left

    return False, None, None


def run():
    # loads all templates from the config
    templates = list(map(lambda path: cv2.imread(path, 0), config_img_csgo_accept_button_paths))

    # every config_refresh a screeshot is taken and a match with the template is searched for
    while True:
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # as gray
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # as RGB

        # for each template, it is checked if there is a match
        for index, template in enumerate(templates):
            try:
                assert (template is not None)  # OpenCV Documentation: If the image cannot be read,
                # the function returns an empty matrix ( Mat::data==NULL ).
            except AssertionError:
                templates.remove(template)
                print("The Template {} could not be loaded and will not be considered anymore.".format(index))
                break

            width, height = template.shape[::-1]
            find, top_left, max_val = find_img_on_screen(image, template, str(index))

            # if a match was found with the threshold value
            if find:
                x = top_left[0] + width / 2
                y = top_left[1] + height / 2
                click_button(x, y, config_click_duration)  # code
                print("Template {} Found and clicked the button.".format(index))

                # if you want to show the screenshot with the match
                if config_show_img:
                    show_image(image_rgb, top_left, width, height, max_val)

                return
        time.sleep(config_refresh)


def click_button(x: int, y: int, t: float):
    pyautogui.click(x, y, duration=t)


def show_image(image_rgb, top_left, width, height, max_val):
    height_rgb, width_rgb = image_rgb.shape[:-1]
    bottom_right = (top_left[0] + width, top_left[1] + height)
    cv2.rectangle(image_rgb, top_left, bottom_right, (0, 0, 255), 10)
    image_rgb = cv2.putText(image_rgb, str("max_val: {}".format(max_val)), (20, int(height_rgb - 100)),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
    image_rgb = cv2.putText(image_rgb, 'Close the window or press the key "0" to continue the program.',
                            (20, int(height_rgb - 50)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (54, 86, 214), 2,
                            cv2.LINE_AA)
    image_rgb = cv2.resize(image_rgb, (int(width_rgb / 1.5), int(height_rgb / 1.5)))
    cv2.imshow('CS:GO Auto Accept: Screenshot where the template was found', image_rgb)
    cv2.waitKey(0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def parse_input(text: str):
    cmd = text.strip().lower()
    for command in COMMANDS:
        if cmd in command[0]:
            func = command[1]
            func()
            # if returned back, then help message
            return
    commands_message()


# revise
def print_commands():
    for command in COMMANDS:
        cmd_string = ""
        for cmd in command[0]:
            cmd_string += f"{cmd} "
        cmd_string += f"-> {command[2]}"
        print(cmd_string)


def commands_message():
    print("\n'start' starts the program\n'cmd' all commands are printed\n'help' the help will be printed\n"
          "'exit' or STRG + C terminates the program\n")


def help_message():
    print("- If no button is detected, set the threshold lower or to 0.6.\n"
          "- Take a screenshot of your accept button and attach it.\n"
          "- Check the config file.\n"
          "- Go to GitHub and create an issue."
          )


def stop():
    print(EXIT_TEXT)
    sys.exit(0)


def start():
    print(START_TEXT)
    commands_message()


COMMANDS = [
    [["start", "s", "run", "r"], run, "starts the program"],
    [["help", "h"], help_message, "the help will be printed"],
    [["exit", "e", "stop", "st"], stop, "terminates the program with status 0"],
    [["command", "commands", "cmd", "c"], print_commands, "all commands are printed"],
    [["loadconfig", "lc"], load_config, "the config is reloaded"]
]

if __name__ == '__main__':
    start()
    load_config()
    while True:
        parse_input(input("> "))
