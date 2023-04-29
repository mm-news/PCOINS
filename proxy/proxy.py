from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    '''request'''

def response(flow: http.HTTPFlow) -> None:
    from functions.functions import getconfig
    body_end = flow.response.content.find(b'</body>')
    replace = open("replace.txt").read().replace(r"{message}", getconfig("string", "message_when_blocked"))
    flow.response.content = flow.response.content[:body_end] + replace.encode() + flow.response.content[body_end:]
