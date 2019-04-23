import usocket as socket

class uWeb:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    OK = b"200 OK"
    NOT_FOUND = b"404 Not Found"
    FOUND = b"302 Found"
    FORBIDDEN = b"403 Forbidden"
    BAD_REQUEST = b"400 Bad Request"
    ERROR = b"500 Internal Server Error"

    def __init__(self, address, port):
        #configure socket
        self.active_socket = socket.socket()

        self.address_info = socket.getaddrinfo(address, port)
        self.address = self.address_info[0][-1]
        print("Bind address info:", self.address_info)

        self.active_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_socket.bind(self.address)
        self.active_socket.listen(5)

    def routes(self, routes={}):
        self.routes_dict = routes

    def router(self):
        if len(self.routes_dict) == 0:
            self.render('welcome.html')
        elif self.resolveRequestLine():
            command, path, http_ver = self.resolveRequestLine()
            if (command, path) in self.routes_dict.keys():
                # check for valid route
                self.routes_dict[(command, path)]()
            elif '.' in path:
                #send file to client
                print('looking for a file')
                self.sendFile(path[1:])
            else:
                self.sendStatus(NOT_FOUND)


    def start(self):
        print("Listening, connect your browser to http://<this_host>:8080/")

        while True:
            connection = self.active_socket.accept()
            self.client_socket = connection[0]
            self.client_address = connection[1]
            print("Client address:", self.client_address)
            print("Client socket:", self.client_socket)

            print("Client Request:")
            self.request_line = self.client_socket.readline()
            print(self.request_line.decode().strip())
            self.extractHeaders()
            print('after req')

            self.router()
            self.client_socket.close()

            print()

    def render(self, html_file, variables=False, status=OK):
        try:
            rendered_content = self.readFile(html_file)
            if variables:
                for var_name, value in variables.items():
                    rendered_content = rendered_content.replace(b"{{%s}}" % var_name, str(value).encode())
            self.sendStatus(status)
            self.sendHeaders({'Content-Type': 'text/html'})
            self.sendBody(b'\n' + rendered_content)
        except Exception as e:
            self.render('500.html', status=self.ERROR)
            print(e)
            print('No such file: %s' % html_file)

    def readFile(self, file):
        with open(file, 'r') as f:
            return ''.join(f.readlines()).encode()

    def sendFile(self, file):
        try:
            to_send = self.readFile(file)
            self.sendStatus(self.OK)
            self.sendBody(to_send)
        except Exception as e:
            self.sendStatus(self.NOT_FOUND)
            print(e)
            print('File: %s was not found, so 404 was sent to client.' % file)

    def sendStatus(self, status_code):
        response_line = b"HTTP/1.1 "
        self.send(response_line + status_code + b'\n')

    def sendHeaders(self, headers_dict):
        self.sendStatus(self.OK)
        for key, value in headers_dict.items():
            self.send(b"%s: %s\n" % (key.encode(), value.encode()))

    def sendBody(self, body_content):
        self.send(b'\n' + body_content)

    def send(self, content):
        self.client_socket.write(content)

    def extractHeaders(self):
        raw_headers = []
        self.request_headers = {}
        while True:
            h = self.client_socket.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h.decode().strip())
            raw_headers.append(h)
        for header in raw_headers:
            split_header = header.decode().strip().split(': ')
            self.request_headers[split_header[0]] = split_header[1]
        print(self.request_headers)

    def resolveRequestLine(self):
        req_line = self.request_line.decode().strip().split(' ')
        if len(req_line) > 1:
            command = req_line[0]
            path = req_line[1]
            http_ver = req_line[2]
            return command, path, http_ver
        else:
            return False

server = uWeb("0.0.0.0", 8080)
def root():
    server.render('content.html')
def header_test():
    server.sendHeaders({
        'adsf': 'yahhh',
        'adwerf': 'yadsfhh',
        'a23f': 'y234h',
    })
server.routes(({
    (uWeb.GET, "/"): root,
    (uWeb.GET, "/header"): header_test
}))
server.start()
