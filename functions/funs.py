"""All functions for the program are here."""
from re import error as re_error
from re import compile as re_compile
from re import search
from functions.errors import HostsListError, ConfigNotFoundError
from functions.cron import global_configs, global_replace, global_hosts, global_ip_dict


def getconfig(section: str, key: str):
    """Get configs."""
    try:
        return global_configs[section][key]
    except KeyError as e:
        raise ConfigNotFoundError(
            f"Config {section}.{key} not found.") from e


def edit_html(html: bytes) -> bytes:
    """Edit html if blocked."""

    body_end = html.rfind(b"</body>")
    replace = global_replace\
        .replace("{message}", getconfig("string", "message_when_blocked"))\
        .replace("<message_block>", "")\
        .replace("</message_block>", "")

    if getconfig("blocking_options", "infinite_alert_loop") == "1":
        replace = replace + """<script>
    function altf() {
        alert({message})
        altf()
    };
    window.onload = function() {
        document.body.style.filter = "blur(5px)";
        window.setTimeout(altf, 500);
    };
</script>""".replace("{message}", getconfig("string", "message_when_blocked"))
    return html[:body_end] + replace.encode() + html[body_end:]


def get_hosts() -> dict:
    """This function returns a dict of hosts.csv."""
    return global_hosts


def get_level(host: str) -> int:
    """This function returns the level of the host."""
    hosts = get_hosts_csv()
    host = host.\
        replace("www.", "").\
        replace("http://", "").\
        replace("https://", "").\
        removesuffix("/")

    def formatting_host(host): return (
        host.startswith("[re]"), host.replace("[re]", ""))

    for hostname, content in hosts.items():
        host_level = content["level"]

        if not hostname.startswith("[re]"):
            ############################# Check without regex #############################

            # check level -3
            if search(hostname, host) and (host_level == -3):
                return -3

            # check level -2
            for j in host.split("."):
                if j in hostname and (host_level == -2):
                    return -2

            # check level -1
            if (hostname == host) and (host_level == -1):
                return -1

            # check level 0
            if (hostname == host) and (host_level == 0):
                return 0

            # check level 1
            if (hostname == host) and (host_level == 1):
                return 1

            # check level 2
            for j in host.split("/"):
                if (j in hostname) and (host_level == 2):
                    return 2

            # check level 3
            if search(hostname, host) and (host_level == 3):
                return 3
        elif hostname.startswith("[re]"):
            ############################# Check with regex #############################

            condition = formatting_host(hostname)[0] and search(
                formatting_host(hostname)[1], host)

            if condition:
                match host_level:
                    # check level -3
                    case -3:
                        return -3

                    # check level -2
                    case -2:
                        return -2

                    # check level -1
                    case -1:
                        return -1

                    # check level 0
                    case 0:
                        return 0

                    # check level 1
                    case 1:
                        return 1

                    # check level 2
                    case 2:
                        return 2

                    # check level 3
                    case 3:
                        return 3

    return 0


def dict_diff(old: dict, new: dict) -> dict:
    diff = {
        "added": {},
        "modified": {},
        "deleted": {}
    }

    for key, value in new.items():
        if isinstance(value, dict):
            if key not in old:
                diff["added"][key] = new[key]
            elif new[key] != old[key]:
                d = dict_diff(old[key], new[key])
                for mk, mv in d.items():
                    if mk == "added":
                        for k, v in mv.items():
                            diff["added"][f"{key}.{k}"] = v
                    elif mk == "modified":
                        for k, v in mv.items():
                            diff["modified"][f"{key}.{k}"] = [v[0], v[1]]
                    elif mk == "deleted":
                        for k, v in mv.items():
                            diff["deleted"][f"{key}.{k}"] = v
        elif key not in old:
            diff["added"][key] = value
        elif value != old[key]:
            diff["modified"][key] = [old[key], value]

    for key in old.keys() - new.keys():
        diff["deleted"][key] = old[key]

    return diff


def adjust_ip(ip): # TODO: split it to adjust_ip and adjust_ip_by_url
    if ip in global_ip_dict.keys():
        return global_ip_dict[ip]

    else:
        get_data_url = functions.getconfig(
            "get_data", "get_by_ip")  # TODO: add cache

        with urllib.request.urlopen(get_data_url+ip) as response:
            content = response.read()

        return content == b"0" # TODO: save it to ip_tmp.csv if we got a result
