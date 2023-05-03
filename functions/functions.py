def getconfig(area:str, name:str):
    from configparser import ConfigParser
    
    config = ConfigParser()
    config.read("./config.ini")
    if area != "" and name != "":
        return config[area][name]
    elif name != "":
        return config[area]
    else:
        return config

def edit_html(html:bytes) -> bytes:
    from functions.functions import getconfig
    body_end = html.find(b'</body>')
    replace = open(getconfig("files", "replace.txt")).read().replace(r"{message}", getconfig("string", "message_when_blocked"))
    return html[:body_end] + replace.encode() + html[body_end:]

def get_hosts_csv() -> dict:
    from functions.functions import getconfig
    from pandas import read_csv

    csv = read_csv(getconfig("files", "hosts_list")[1:-1])

    hosts = {}

    for i in csv.values:
        hosts[i[0]] = {
            "level": i[1],
            "reason": i[2],
            "comment": i[3]
        }
    return hosts
