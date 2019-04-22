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

    def __init__(self):

        self.active_socket = socket.socket()

        self.address_info = socket.getaddrinfo("0.0.0.0", 8080)
        self.address = self.address_info[0][-1]
        print("Bind address info:", self.address_info)

        self.active_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_socket.bind(self.address)
        self.active_socket.listen(5)

    def rootAction(self):
        self.render('welcome.html')

    def routes(self, routes={(GET, "/"): rootAction}):
        self.routes_dict = routes

    def router(self):
        if self.resolveRequestLine():
            command, path, http_ver = self.resolveRequestLine()
            # print(self.routes.keys())
            if (command, path) in self.routes_dict.keys():
                self.routes_dict[(command, path)](self)
            else:
                self.render('404.html', status=self.NOT_FOUND)

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
            print(self.request_line)
            while True:
                h = self.client_socket.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)
            print('after req')

            self.router()
            self.client_socket.close()

            print()



    def render(self, html_file, variables=False, status=OK):
        response_line = b"HTTP/1.0 "
        try:
            rendered_content = self.readFile(html_file)
        except Exception as e:
            status = NOT_FOUND
            print(e)

        if variables:
            for var_name, value in variables.items():
                rendered_content = rendered_content.replace(b"{{%s}}" % var_name, str(value).encode())

        self.client_socket.write(response_line + status + b'\r\n\n' + rendered_content)
        print('response', response_line + status + b'\r\n\n' + rendered_content)

    def readFile(self, file):
        with open(file, 'r') as f:
            return ''.join(f.readlines()).encode()

    def resolveRequestLine(self):
        req_line = self.request_line.decode().strip().split(' ')
        if len(req_line) > 1:
            command = req_line[0]
            path = req_line[1]
            http_ver = req_line[2]
            return command, path, http_ver
        else:
            return False

server = uWeb()
def root(self):
    self.render('content.html')
server.routes({
    (uWeb.GET, "/"): root
})
server.start()
