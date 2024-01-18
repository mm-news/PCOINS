# Proxy-based Control Of Internet Navigation System (PCOINS)

![GitHub](https://img.shields.io/github/license/Studio-Undefined/PCOINS?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/Studio-Undefined/PCOINS?style=flat)

```text

    ______    _____    ____    _____  __    __  ______  
   |  ___ \  /  ___| /  ___ \ |_   _||  \  | | / _____\  
   | |___| ||  /    / /  _ \ \  | |  | \ \ | |/ /______  
  _|  ____/_| |    | |  |_| | | | |  | |\ \| |\______  \    ________  
 / | |     /|  \___ \ \____/ / _| |_ | | \ \ | _____/  /  / v0.1.0 /  
/__|_|____/__\_____|_\______/_|_____||_|__\_\|_\______/__/________/  

```

## What Is This

Proxy-based Control Of Internet Navigation System (PCOINS) is an AI-powered system to control students’ internet activity with mitmproxy.  
In this system, you will have a website to access settings and students’ activity.  
There will be an AI model that can identify whether the website that students going to is illegal or not, If the AI thinks the website is very likely illegal,  
the AI will stop the request and replace it with a page so make teacher can preview the website and decide to let the student access the page or not.

## Requirements

see at /requirements.txt

## Columns of hosts.csv

### Column: Host

The host of the website. (String)  
e.g.  

- bing,  
- github.com,  
- studio-undefined.github.io,  
- [re]*.google.com,
etc.

If starts with `[re]`, it will be treated as a regular expression.  
**Note: do not include the protocol (e.g. https://) and the path (e.g. /search?q=hello).**

### Column: Level

The level of the website. (Integer)  
e.g.  
1, 2, 3, 4, 5  

### **Levels:**

| Level |            Description            |
|:------|:---------------------------------:|
|-3     |  Allow URLs that includes {Host}  |
|-2     |         Allow \*.{Host}.\*        |
|-1     |           Allow {Host}            |
|0      |          Normal: Allow            |
|1      |           Block {Host}            |
|2      |       Block \*.{Host}.\*          |
|3      | Block URLs that includes {Host}   |

{Host} is the host of the website.  
Hint: This program will check the level from -2 to 2.  
If the level is -1, the program will stop checking and allow the request.

### Column: Reason

e.g. games, education, etc.  
The reason the website is blocked (or allowed). (String)

### Column: Comment

e.g. for testing, etc.  
Other comments. (String)

## How to config config.ini

### Section: \[string\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| message_when_blocked | String |    *     | "You were blocked from accessing this website." | The message will be shown when the website is blocked. |

### Section: \[get_data\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| get_data_function_on | Boolean(0/1) |    *     | 0 | Whether to get data from given url. |
| get_by_ip | url |  -  | None | The url to get data by ip, ip address will be appended to the end of the url. The url should return 0 if the ip is not blocked, 1 if the ip is blocked. |

### Section: \[numbers\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| config_refresh_interval | Integer |    *     | 3 | The interval of refreshing the config file (in minutes).  Set this to -1 to disable refreshing. **cron.py will not refresh this option automatically.** |
| replace_refresh_interval | Integer |    *     | 3 | The interval of refreshing the replace.txt file (in minutes).  Set this to -1 to disable refreshing. **cron.py will not refresh this option automatically.** |
| hosts_refresh_interval | Integer |    *     | 1 | The interval of refreshing the hosts.csv file (in minutes).  Set this to -1 to disable refreshing. **cron.py will not refresh this option automatically.** |
| ip_dict_refresh_interval | Integer |    *     | 1 | The interval of reading the ip dict (in minutes).  Set this to -1 to disable refreshing. **cron.py will not refresh this option automatically.** |

### Section: \[files\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| replace.txt | Path |    *     | replace.txt | The path of the replace.txt file. |
| host_list | Path |    *     | hosts.csv | The path of the hosts.csv file. |

### Section: \[blocking_options\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| shutdown_html_when_blocked | Boolean(0/1) |    *     | 0 | Whether to shutdown the html when blocked. |
| shutdown_all_things_when_blocked | Boolean(0/1) |    *     | 0 | Whether to shutdown all things when blocked.(including html, csv, websocket, etc.) |
| infinite_alert_loop | Boolean(0/1) |    *     | 1 | Whether to alert the user infinitely so the user can't access the website normally. (If the user turned of JavaScript, this option will be useless.) |
| cover_window | Boolean(0/1) |    *     | 1 | Whether to cover the window with a blur div. |
| refresh_interval | Integer |    -     | 5 | The interval of refreshing the website to make sure the user can't access the website normally. (in seconds) |

### Section: \[mode\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| blacklist_mode | Boolean(0/1) |    *     | 1 | PCOINS will only block the websites with level >= 1. |
| whitelist_mode | Boolean(0/1) |    *     | 0 | PCOINS will only allow the websites with level <= 1. |

### Section: \[others\]

| Name |  Type  | Required | Default | Description |
|:-----|:-------|:--------:|:-------:|:------------|
| colorful | Boolean(0/1) |    *     | 1 | COLORFUL output!  **The LOGO will be colorful even if this option is set to 0.** |
