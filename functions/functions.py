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