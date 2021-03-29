import pyautogui
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import sys
from configparser import ConfigParser
import json

config_refresh = 1
config_threshold = 0.6
config_img_csgo_accept_button_paths: []
config_click_duration = 0.2
config_show_img = False

START_TEXT = "CS:GO Auto Accept - V 1.0"


# github: tym21

def load_config():
    global config_refresh
    global config_img_csgo_accept_button_paths
    global config_threshold
    global config_click_duration
    global config_show_img

    config = ConfigParser()
    config.read("config.ini")
    config_refresh = int(config["DEFAULT"]["refresh"])
    config_img_csgo_accept_button_paths = json.loads(config.get("DEFAULT", "img_csgo_accept_button_path"))
    config_threshold = float(config["DEFAULT"]["threshold"])
    config_click_duration = float(config["DEFAULT"]["click_duration"])
    config_show_img = config["DEFAULT"].getboolean("show_img")

    print(f"Config loaded: {config_refresh=} {config_threshold=} {config_click_duration=} {config_show_img=} {config_img_csgo_accept_button_paths=}")


def find_img_on_screen(image, template, name=""):
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(f"Template {name}: {max_val=}")
    if max_val >= config_threshold:
        top_left = max_loc
        return True, top_left

    return False, None


def click_button(x: int, y: int, t: float):
    pyautogui.click(x, y, duration=t)


def run():
    # loads all templates from the config
    templates = list(map(lambda path: cv2.imread(path, 0), config_img_csgo_accept_button_paths))

    while True:
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # as black white
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for index, template in enumerate(templates):
            width, height = template.shape[::-1]
            find, top_left = find_img_on_screen(image, template, str(index))
            if find:
                x = top_left[0] + width / 2
                y = top_left[1] + height / 2
                click_button(x, y, config_click_duration)  # code
                print(index, "Found the button and clicked.")

                if config_show_img:
                    bottom_right = (top_left[0] + width, top_left[1] + height)
                    cv2.rectangle(img_rgb, top_left, bottom_right, (255, 0, 0), 10)
                    plt.title("Screenshot")
                    plt.imshow(img_rgb)
                    plt.show()

                return

        time.sleep(config_refresh)


def parse_input(text: str):
    cmd = text.strip().lower()
    for command in COMMANDS:
        if cmd in command[0]:
            func = command[1]
            func()


def help_message():
    print("'start' starts the program\n'cmd' all commands are printed\n'exit' terminates the program")


# revise
def print_commands():
    for command in COMMANDS:
        cmd_string = ""
        for cmd in command[0]:
            cmd_string += f"{cmd} "
        cmd_string += f"-> {command[2]}"
        print(cmd_string)


def stop():
    print("goodbye.")
    sys.exit(0)


def start():
    print(START_TEXT)


COMMANDS = [
    [["start", "s", "run", "r"], run, "starts the program"],
    [["help", "h"], help_message, "the help will be printed"],
    [["exit", "e", "stop", "st"], stop, "terminates the program with status 0"],
    [["command", "commands", "cmd", "c"], print_commands, "all commands are printed"],
    [["load config", "lc"], load_config, "the config is reloaded"]
]

if __name__ == '__main__':
    load_config()
    start()
    help_message()
    while True:
        parse_input(input("> "))
