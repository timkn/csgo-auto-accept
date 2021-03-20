import pyautogui
import cv2
import numpy
import time
import sys
from configparser import ConfigParser

config_language = "EN"
config_refresh = 1
WELCOME_TEXT = "CS:GO Auto Accept - V 1.0"
INFO_TEXT = 'type "start" to run the program'


def load_config():
    global config_language
    global config_refresh
    config = ConfigParser()
    config.read("config.ini")
    config_language = config["DEFAULT"]["language"]
    config_refresh = config["DEFAULT"]["refresh"]


def run():
    pass


def parse_input(text: str):
    cmd = text.strip().lower()
    if cmd == "start":
        run()
    elif cmd == "help":
        help_message()


def help_message():
    print("Commands: 'start' the program starts")


def start():
    print(WELCOME_TEXT)
    print(f"Config loaded: language = {config_language}; refresh = {config_refresh}")
    print(INFO_TEXT)


if __name__ == '__main__':
    load_config()
    start()
    while True:
        parse_input(input("> "))
