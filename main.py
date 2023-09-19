"""Run this file to start the proxy server."""
# pylint: disable=W1401
import threading
import datetime
import time
import sys
from mitmproxy.tools.main import mitmdump
from functions.custom_classes import ColorfulText, TextColors, colorful_print
sys.dont_write_bytecode = True

print("""\x1b[1;32;40m

    ______    _____    ____    _____  __    __  ______ 
   |  ___ \  /  ___| /  ___ \ |_   _||  \  | | / _____\ 
   | |___| ||  /    / /  _ \ \  | |  | \ \ | |/ /______ 
  _|  ____/_| |    | |  |_| | | | |  | |\ \| |\______  \    ________ 
 / | |     /|  \___ \ \____/ / _| |_ | | \ \ | _____/  /  / v0.1.0 / 
/__|_|____/__\_____|_\______/_|_____||_|__\_\|_\______/__/________/ 

\x1b[0m""")

# input("Please remember to run web_worker.py! If you did, press ENTER> \n")

# Setup colorful text
CC = ColorfulText
ts = TextColors.TextStyle
tc = TextColors.Color
tbc = TextColors.BackgroundColor
cp = colorful_print

# self-check
print(CC("==========================SELF-CHECK==========================",
      color=tc.Y))
try:
    print(f"{CC('TIME', color=tc.BL)}: {datetime.datetime.now().ctime()}")

    # check funs.py

    cp("Importing functions......", "PROCESSING")
    import functions.funs as functions  # noqa: E402
    cp("Importing functions......OK", "SUCCESS")

    # check files
    cp("Checking all files......\r", "PROCESSING", end="")
    open(functions.getconfig("files", "hosts_list")[1:-1], encoding="utf-8")
    open(functions.getconfig("files", "replace.txt")[1:-1], encoding="utf-8")
    cp("Checking all files......OK", "SUCCESS")

    # check hosts.csv
    cp("Checking hosts.csv......\r", "PROCESSING", end="")
    functions.get_hosts()
    cp("Checking hosts.csv......OK", "SUCCESS")
except Exception as e:
    cp(f"ERROR: {e}", "ERROR")
    print(CC("==============================================================",
          ts.B, tc.Y, tbc.BK))
    cp("FAILED. Please fix the error and try again.",
       "ERROR")
    raise SystemExit from e
cp("SELF-CHECK: OK", "SUCCESS")
print(CC("==============================================================",
      ts.B, tc.Y, tbc.BK))
cp("\nSelf-check finished. Starting......\n", "PROCESSING")
print(CC("==============================================================",
      ts.B, tc.G, tbc.BK))

cp("Setting up proxy......\r",
   "PROCESSING", end="")


def start_proxy():
    """Start proxy."""
    mitmdump(args=["-s", "./proxy/proxy.py"])


cp("Setting up cron......\r",
   "PROCESSING", end="")
# pylint: disable=import-outside-toplevel, wrong-import-position
from functions import cron  # noqa: E402

cron_worker = threading.Thread(target=cron.start_cron)
cp("Setting up cron......OK",
   "SUCCESS")

cp("Starting cron......\r", "PROCESSING", end="")
cron_worker.start()
cp("Starting cron......OK", "SUCCESS")

cp("Starting proxy......", "PROCESSING")

print(CC("==============================================================\n",
      ts.B, tc.G, tbc.BK))

start_proxy()

wait_timer = 0.0
print(CC("Waiting for cron to stop......\r",
      color=tc.C), end="")
while cron_worker.is_alive():
    print(
        CC(f"Waiting for cron to stop, \
this might take about 30 seconds......{wait_timer:.1f}sec.\r",
           color=tc.C), end="")
    cron.set_stop_cron()
    if wait_timer >= 30:
        cp("Waiting for cron to stop......TIMEOUT"+" "*50,
            "ERROR")
        cp("Please stop cron manually.",
           "ERROR")
        break
    time.sleep(0.5)
    wait_timer = wait_timer + 0.5
cp("Waiting for cron to stop......OK"+" "*50,
   "SUCCESS")
sys.exit(0)
