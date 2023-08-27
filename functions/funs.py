"""All functions for the program are here."""
from configparser import ConfigParser
from re import error as re_error
from re import compile as re_compile
from re import search
from pandas import read_csv
from functions.errors import HostsListError

def getconfig(area: str, name: str):
    """Get config from config.ini."""
    config = ConfigParser()
    config.read("./config.ini")

    if area != "" and name != "":
        return config[area][name]
    elif name != "":
        return config[area]
    else:
        return config


def edit_html(html: bytes) -> bytes:
    """Edit html if blocked."""

    body_end = html.rfind(b"</body>")
    replace = open(getconfig("files", "replace.txt",)[
                   1:-1]
                , encoding="utf-8")\
                .read()\
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


def get_hosts_csv() -> dict:
    """This function returns a dict of hosts.csv."""
    csv = read_csv(getconfig("files", "hosts_list")[1:-1])

    hosts = {}

    for i in csv.values:
        if i[0].startswith("https://") or i[0].startswith("http://"):
            raise HostsListError(
                f"Hosts list contains http:// or https:// in {i[0]}")
        if "*" in i[0] and not i[0].startswith("[re]"):
            raise HostsListError(
                f"Hosts list contains * but without [re] in {i[0]}")
        if i[0].endswith("/"):
            raise HostsListError(f"Hosts list ends with / in {i[0]}")
        if i[1] not in [-3, -2, -1, 0, 1, 2, 3]:
            raise HostsListError(f"Hosts list contains invalid level in {i[0]}")
        if not isinstance(i[0], str):
            raise HostsListError(f"Hosts list contains invalid host in {i[0]}")
        if not isinstance(i[1], int):
            raise HostsListError(f"Hosts list contains invalid level in {i[0]}")
        if i[0].startswith("[re]"):
            try:
                re_compile(i[0].replace("[re]", ""))
            except re_error as reerror:
                raise re_error(
                    f"RE ERROR AT HOST{i[0]}: {reerror}") from reerror
        hosts[i[0]] = {
            "level": i[1],
            "reason": i[2],
            "comment": i[3]
        }
    return hosts


def get_level(host: str) -> int:
    """This function returns the level of the host."""
    hosts = get_hosts_csv()
    host = host.\
        replace("www.", "").\
        replace("http://", "").\
        replace("https://", "").\
        removesuffix("/")

    formatting_host = lambda host : (host.startswith("[re]"), host.replace("[re]", ""))

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
