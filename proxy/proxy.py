'''Proxy Scripts'''
from re import error as re_error
from mitmproxy import http
import functions.functions as functions

def request(flow: http.HTTPFlow) -> None:
    '''request'''

def response(flow: http.HTTPFlow) -> None:
    '''response'''
    try:

        host = flow.request.host.split(":")[0]

        html = flow.response.content

        level = functions.get_level(host)

        kill_html = functions.getconfig("blocking_options", "shutdown_html_when_blocked")
        kill_other = functions.getconfig("blocking_options", "shutdown_other_things_when_blocked")

        if (level > 0 and functions.getconfig("blocking_options", "refresh_interval_when_blocked") != "-1"):
            if "Refresh" in flow.response.headers.keys():
                flow.response.headers["Refresh"] = functions.getconfig("blocking_options", "refresh_interval")
            else:
                flow.response.headers["Refresh"] = functions.getconfig("blocking_options", "refresh_interval")

        match level:
            case -3:
                print(-3) #debug
            case -2:
                print(-2) #debug
                return
            case -1:
                print(-1) #debug
                return
            case 0:
                print(0) #debug
                return
            case 1:
                print(1) #debug
                if "text/html" in flow.response.headers["content-type"]:
                    if kill_html == "1":
                        flow.kill()
                    flow.response.content = functions.edit_html(html)
                elif kill_other == "1":
                    flow.kill()
                return
            case 2:
                print(2) #debug
                if "text/html" in flow.response.headers["content-type"]:
                    if kill_html == "1":
                        flow.kill()
                    flow.response.content = functions.edit_html(html)
                elif kill_other == "1":
                    flow.kill()
                return
            case 3:
                print(3) #debug
                if "text/html" in flow.response.headers["content-type"]:
                    if kill_html == "1":
                        flow.kill()
                    flow.response.content = functions.edit_html(html)
                elif kill_other == "1":
                    flow.kill()
                return
        return
    except re_error as error:
        print(f"RE ERROR: {error}")
    except Exception as error:
        print(f"ERROR: {error}")
        return
