from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    """request"""

def response(flow: http.HTTPFlow) -> None:
    from bs4 import BeautifulSoup
    
    if flow.response and flow.response.content:
        body_tag = BeautifulSoup(flow.response.content)
        body_tag.find("body")
        print(body_tag)
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