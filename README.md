# Python Control Of Internet Navigation System (PCOINS)

## What Is This

Python Control Of Internet Navigation System (PCOINS) is an AI powered system to control students’ internet activity with mitmproxy.  
In this system, you will have a website to access settings and students’ activity.  
There will be an AI model can identify the website that students’ going to is an illegal website or not, if the AI think the website is very likely an illegal website,  
the AI will stop the request and replace it with a page to make teacher can preview the website and decide to let the student access the page or not.

## TODO

1. proxy 控制系統
2. AI 網頁分析
3. web前台

## Requirements

see at /requirements.txt

## Columns of hosts.csv

### column: Host

The host of the website. (String)  
e.g. google.com or www.google.com  
**DONT** DO THIS: "http://google.com/" or "*.google.com"  

### column: Level

The level of the website. (Integer)  
e.g. 1, 2, 3, 4, 5  

### **Levels:**

| Level |           Description          |
|:------|:------------------------------:|
|-1     |    Whitelist: Always Allowed   |
|0      |         Normal: Allowed        |
|1      |          Block {Host}          |
|2      |         Block {Host}.*         |
|3      |      Block \*.{Host}.\*        |

{Host} is the host of the website.  
Hint: this program will check the level from -1 to 3.  
If the level is -1, the program will stop checking and allow the request.

### column: Reason

The Reason of the website is blocked (or allowed). (String)

### column: Comment

Other comments. (String)
