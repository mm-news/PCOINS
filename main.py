"""Run this file to start the proxy server."""

import datetime
from mitmproxy.tools.main import mitmdump
import functions.functions as functions

#input("Please remember to run web_worker.py! If you did, press ENTER> ")

# self-check
print("==========================SELF-CHECK==========================")
try:
    print(f"TIME: {datetime.datetime.now().ctime()}")

    #check files
    print("Checking all files......")
    open(functions.getconfig("files", "hosts_list")[1:-1], encoding="utf-8")
    open(functions.getconfig("files", "replace.txt")[1:-1], encoding="utf-8")
    print("Checking all files......OK")

    #check hosts.csv
    print("Checking hosts.csv......")
    functions.get_hosts_csv()
    print("Checking hosts.csv......OK")

except Exception as e:
    print(f"ERROR: {e}")
    print("==============================================================")
    print("FAILED. Please fix the error and try again.")
    raise SystemExit from e
print("SELF-CHECK: OK")
print("==============================================================")

mitmdump(args=["-s", "./proxy/proxy.py"])
