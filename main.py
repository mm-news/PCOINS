from mitmproxy.tools.main import mitmdump

input("Please remember to run web_worker.py! If you did, press ENTER> ")
mitmdump(args=["-s", "./proxy/proxy.py"])
