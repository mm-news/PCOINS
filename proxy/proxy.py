'''Proxy Scripts'''
from re import error as re_error
from mitmproxy import http
from urllib import request
import functions.funs as functions


def request(flow: http.HTTPFlow) -> None:
    '''request'''
    if functions.getconfig("get_data", "get_data_functions_on") == "0":
        return
    get_data_url = functions.getconfig(
        "get_data", "get_by_ip")

    with urllib.request.urlopen(get_data_url+flow.client_conn.ip_address) as response:
        content = response.read()
        if content == b"0":
            return
        else:
            flow.kill()


def response(flow: http.HTTPFlow) -> None:
    '''response'''
    try:

        host = flow.request.host.split(":")[0]

        html = flow.response.content

        level = functions.get_level(host)

        kill_html = functions.getconfig(
            "blocking_options", "shutdown_html_when_blocked")
        kill_other = functions.getconfig(
            "blocking_options", "shutdown_all_things_when_blocked")

        if (level > 0 and functions.getconfig("blocking_options", "refresh_interval") != "-1"):
            flow.response.headers["refresh"] = functions.getconfig(
                "blocking_options", "refresh_interval")

        match level:
            case -3:
                print(-3)  # debug
            case -2:
                print(-2)  # debug
                return
            case -1:
                print(-1)  # debug
                return
            case 0:
                print(0)  # debug
                return
            case 1:
                print(1)  # debug
                if "text/html" in flow.response.headers["content-type"]:
                    if kill_html == "1":
                        flow.kill()
                    flow.response.content = functions.edit_html(html)
                elif kill_other == "1":
                    flow.kill()
                return
            case 2:
                print(2)  # debug
                if "text/html" in flow.response.headers["content-type"]:
                    if kill_html == "1":
                        flow.kill()
                    flow.response.content = functions.edit_html(html)
                elif kill_other == "1":
                    flow.kill()
                return
            case 3:
                print(3)  # debug
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
