"""Run this file to start the proxy server."""
# pylint: disable=W1401
import threading
import datetime
import time
import sys
from mitmproxy.tools.main import mitmdump

print("""

    ______    _____    ____    _____  __    __  ______ 
   |  ___ \  /  ___| /  ___ \ |_   _||  \  | | / _____\ 
   | |___| ||  /    | /  _ \ |  | |  | \ \ | |/ /______ 
  _|  ____/_| |     | | |_|| |  | |  | |\ \| |\______  \    ________ 
 / | |     /|  \___ | \____/ | _| |_ | | \ \ | _____/  /  / v0.1.0 / 
/__|_|____/__\_____|_\______/_|_____||_|__\_\|_\______/__/________/ 

""")

# input("Please remember to run web_worker.py! If you did, press ENTER> ")

# self-check
print("==========================SELF-CHECK==========================")
try:
    print(f"TIME: {datetime.datetime.now().ctime()}")

    # check funs.py

    print("Importing functions......")
    import functions.funs as functions  # noqa: E402
    print("Importing functions......OK")

    # check files
    print("Checking all files......\r", end="")
    open(functions.getconfig("files", "hosts_list")[1:-1], encoding="utf-8")
    open(functions.getconfig("files", "replace.txt")[1:-1], encoding="utf-8")
    print("Checking all files......OK")

    # check hosts.csv
    print("Checking hosts.csv......\r", end="")
    functions.get_hosts_csv()
    print("Checking hosts.csv......OK")
except Exception as e:
    print(f"ERROR: {e}")
    print("==============================================================")
    print("FAILED. Please fix the error and try again.")
    raise SystemExit from e
print("SELF-CHECK: OK")
print("==============================================================")
print("\nSelf-check finished. Starting proxy......\n")
print("==============================================================")

print("Setting up proxy......\r", end="")


def start_proxy():
    """Start proxy."""
    mitmdump(args=["-s", "./proxy/proxy.py"])


print("Setting up cron......\r", end="")
# pylint: disable=import-outside-toplevel, wrong-import-position
from functions import cron  # noqa: E402

cron_worker = threading.Thread(target=cron.start_cron)
print("Setting up cron......OK")

print("Starting cron......\r", end="")
cron_worker.start()
print("Starting cron......OK")

print("Starting proxy......\r", end="")

print("==============================================================\n")

start_proxy()

wait_timer = 0.0
print("Waiting for cron to stop......\r", end="")
while cron_worker.is_alive():
    print(f"Waiting for cron to stop......{wait_timer}sec.\r", end="")
    cron.set_stop_cron()
    if wait_timer >= 10:
        print("Waiting for cron to stop......TIMEOUT")
        print("Please stop cron manually.")
        break
    time.sleep(0.5)
    wait_timer = wait_timer + 0.5
print("Waiting for cron to stop......OK               ")
sys.exit(0)
