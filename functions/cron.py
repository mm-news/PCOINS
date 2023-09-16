"""This file contains the cron functions."""
# pylint: disable=C0103, W0603, W0212
import time
import difflib
from configparser import ConfigParser

global_configs = None
global_replace = None

stop_cron = False


def refresh_configs():
    """Refresh configs."""
    global global_configs
    config_parser = ConfigParser()
    config_parser.read("./config.ini")
    if global_configs == config_parser._sections:
        print("Configs not changed.")
        return
    elif global_configs is not None:
        print(
            f"Refreshing Config. Difference: {', '.join(difflib.ndiff(config_parser._sections, global_configs))}")

        global_configs = config_parser._sections

        print("Configs refreshed.")
        return
    else:
        global_configs = config_parser._sections
        print("Configs loaded.")
        return


def refresh_replace():
    """Refresh replace.txt"""
    global global_replace
    replace = open(global_configs["files"]
                   ["replace.txt"][1:-1], encoding="utf-8")
    if global_replace == replace.read():
        print("replace.txt not changed.")
        replace.close()
        return
    elif global_replace is not None:
        print(
            f"Refreshing replace.txt. Difference: {', '.join(difflib.context_diff(replace.read(), global_replace))}")

        global_replace = replace.read()

        print("replace.txt refreshed.")
        return
    else:
        global_replace = replace.read()
        print("replace.txt loaded.")
        return


def start_cron():
    """Start cron."""
    t = 0
    while True:
        if t % int(global_configs["numbers"]["config_refresh_interval"])*60 == 0:
            refresh_configs()
            t = 0

        if stop_cron:
            break
        time.sleep(3)
        t += 3


def set_stop_cron():
    """Set stop cron."""
    global stop_cron
    stop_cron = True


refresh_configs()
# TODO: REMEMBER to close replace.txt in the function!!!
# TODO: start_cron is incompeleted
