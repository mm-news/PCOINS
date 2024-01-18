"""This file contains the cron functions."""
# pylint: disable=C0103, W0603, W0212
import time
import difflib
import csv
from configparser import ConfigParser

global_configs = None
global_replace = None
global_hosts = None
global_ip_dict = None

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
        from functions.funs import dict_diff  # noqa: E402

        differences = dict_diff(global_configs, config_parser._sections)

        print("Config changed. Difference:")

        if differences["added"]:
            print("added:")
            for key in differences["added"]:
                print(f"{key}: {differences['added'][key]}")

        if differences["modified"]:
            print("modified:")
            for key in differences["modified"]:
                print(
                    f"{key}: {differences['modified'][key][0]} -> {differences['modified'][key][1]}")

        if differences["deleted"]:
            print("deleted:")
            for key in differences["deleted"]:
                print(f"{key}: {differences['deleted'][key]}")

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
    if global_replace is None:
        global_replace = replace.read()
        print("replace.txt loaded.")
        replace.close()
        return
    elif global_replace == replace.read():
        print("replace.txt not changed.")
        replace.close()
        return
    elif global_replace != replace.read():
        print(
            f"Refreshing replace.txt. \
Difference: {difflib.SequenceMatcher(None, global_replace, replace.read()).ratio()}")

        global_replace = replace.read()

        print("replace.txt refreshed.")
        replace.close()
        return


def refresh_hosts():
    """Refresh hosts."""
    global global_hosts
    hosts = open(global_configs["files"]["hosts_list"][1:-1], encoding="utf-8")
    host_list = format_host([i for i in csv.reader(hosts)])
    if global_hosts is None:
        global_hosts = host_list
        print("hosts loaded.")
        hosts.close()
        return
    elif global_hosts == host_list:
        print("hosts not changed.")
        hosts.close()
        return
    elif global_hosts != host_list:
        from functions.funs import dict_diff  # noqa: E402
        differences = dict_diff(global_hosts, host_list)
        print("Refreshing hosts...\r", end="")
        global_hosts = host_list
        print("hosts refreshed. Difference:"+" "*50)
        if differences["added"]:
            print("added:")
            for key in differences["added"]:
                print(f"{key}: {differences['added'][key]}")
        if differences["modified"]:
            print("modified:")
            for key in differences["modified"]:
                print(
                    f"{key}: {differences['modified'][key][0]} -> {differences['modified'][key][1]}")
        if differences["deleted"]:
            print("deleted:")
            for key in differences["deleted"]:
                print(f"{key}: {differences['deleted'][key]}")
        hosts.close()
        return


def refresh_ip_dict():
    from functions.funs import adjust_ip  # noqa: E402

    global global_ip_dict
    global_ip_dict = {}
    ip_dict_tmp = []
    import csv

    with open(global_configs["files"]["ip_tmp_list"][1:-1], encoding="utf-8") as f:
        ip_dict_tmp = [i for i in csv.reader(f)]

    ip_dict = {}
    updated = 0

    for i in global_ip_dict.keys():
        a = adjust_ip(i)
        if global_ip_dict[i] != a:
            ip_dict[i] = a
            updated += 1
        else:
            pass

    for i in ip_dict_tmp:
        ip_dict[i[0]] = i[1]
        updated += 1

    global_ip_dict = ip_dict

    print(f"IP dict refreshed. {updated} IPs updated.")

    return


def format_host(host: list) -> dict:
    from functions.errors import HostsListError  # noqa: E402
    from re import error as re_error, compile as re_compile  # noqa: E402
    formatted_hosts = {}

    for i in host[1:]:
        try:
            i[1] = int(i[1])
        except TypeError as typeerror:
            raise HostsListError(
                f"Hosts list contains invalid level in {i}") from typeerror
        except ValueError as valueerror:
            raise HostsListError(
                f"Hosts list contains invalid level in {i}") from valueerror
        finally:
            if i[0].startswith("https://") or i[0].startswith("http://"):
                raise HostsListError(
                    f"Hosts list contains http:// or https:// in {i[0]}")
            if "*" in i[0] and not i[0].startswith("[re]"):
                raise HostsListError(
                    f"Hosts list contains * but without [re] in {i[0]}")
            if i[0].endswith("/"):
                raise HostsListError(f"Hosts list ends with / in {i[0]}")
            if i[1] not in [-3, -2, -1, 0, 1, 2, 3]:
                raise HostsListError(
                    f"Hosts list contains invalid level in {i[0]}")
            if not isinstance(i[0], str):
                raise HostsListError(
                    f"Hosts list contains invalid host in {i[0]}")
            if i[0].startswith("[re]"):
                try:
                    re_compile(i[0].replace("[re]", ""))
                except re_error as reerror:
                    raise re_error(
                        f"RE ERROR AT HOST{i[0]}: {reerror}") from reerror
            formatted_hosts[i[0]] = {
                "level": i[1],
                "reason": i[2],
                "comment": i[3]
            }
    return formatted_hosts


def start_cron():
    """Start cron."""
    ct = 0  # refresh configs
    rt = 0  # refresh replace
    ht = 0  # refresh hosts
    it = 0  # refresh ip dict

    while True:
        if ct >= int(global_configs["numbers"]["config_refresh_interval"])*60 and \
                int(global_configs["numbers"]["config_refresh_interval"]) != -1:
            refresh_configs()
            ct = 0

        if rt >= int(global_configs["numbers"]["replace_refresh_interval"])*60 and \
                int(global_configs["numbers"]["replace_refresh_interval"]) != -1:
            refresh_replace()
            rt = 0

        if ht >= int(global_configs["numbers"]["hosts_refresh_interval"])*60 and \
                int(global_configs["numbers"]["hosts_refresh_interval"]) != -1:
            refresh_hosts()
            ht = 0

        if it >= int(global_configs["numbers"]["ip_dict_refresh_interval"])*60 and \
                int(global_configs["numbers"]["ip_dict_refresh_interval"]) != -1:
            refresh_ip_dict()
            it = 0

        if stop_cron:
            break

        time.sleep(5)

        ct += 5
        rt += 5
        ht += 5
        it += 5


def set_stop_cron():
    """Set stop cron."""
    global stop_cron
    stop_cron = True


refresh_configs()
refresh_replace()
refresh_hosts()
