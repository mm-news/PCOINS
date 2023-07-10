# Python Control Of Internet Navigation System (PCOINS)

## What Is This

Python Control Of Internet Navigation System (PCOINS) is an AI-powered system to control students’ internet activity with mitmproxy.  
In this system, you will have a website to access settings and students’ activity.  
There will be an AI model can identify the website that students’ going to is an illegal website or not, if the AI thinks the website is very likely illegal,  
the AI will stop the request and replace it with a page to make teacher can preview the website and decide to let the student access the page or not.

## TODO

1. proxy 控制系統
2. AI 網頁分析
3. web 前台

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

if starts with `[re]`, it will be treated as a regular expression.  
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
Hint: this program will check the level from -2 to 2.  
If the level is -1, the program will stop checking and allow the request.

### Column: Reason

e.g. games, education, etc.  
The reason the website is blocked (or allowed). (String)

### Column: Comment

e.g. for testing, etc.  
Other comments. (String)

## config.ini

### Section: \[string\]

#### Option: message_when_blocked

The message will be shown when the website is blocked. (String)

### Section: \[files\]

#### Option: replace.txt

The file content will be added to the end of the blocked website. (String)

#### Option: hosts.csv

The file path of the hosts.csv. (String)
