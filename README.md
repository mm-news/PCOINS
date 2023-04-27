# Python Control Of Internet Navigation System (PCOINS)
## What is this
Python Control Of Internet Navigation System (PCOINS) is an AI powered system to control students’ internet activity with mitmproxy.
In this system, you will have a website to access settings and students’ activity.
There will be an AI model can identify the website that students’ going to is an illegal website or not, if the AI think the website is very likely an illegal website, the AI will stop the request and replace it with a page to make teacher can preview the website and decide to let the student access the page or not.
## TODO
1. ~DNS~ PROXY控制系統
2. AI 網頁分析
3. web前台
## requirements
1. python3 (anaconda)
2. psycopg2
3. flask
4. flask-login
5. ~dnslib~ mitmproxy
