'''Proxy Scripts'''
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    '''request'''

def response(flow: http.HTTPFlow) -> None:
    '''response'''
    if "text/html" in flow.response.headers["content-type"]:
        import functions.functions as functions

        host = flow.request.host

        if host in functions.get_hosts_csv():
            level = functions.get_hosts_csv()[host]["level"]
            if level <= 0:
                return
            elif level >= 1:
                flow.response.content = functions.edit_html(flow.response.content)
                return
        else:
            return
            
