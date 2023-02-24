from mitmproxy.tools.main import mitmdump

input("Please remember to run web.py! If you did, press ENTER> ")
mitmdump(args=["-s", "./workers/proxy.py"])