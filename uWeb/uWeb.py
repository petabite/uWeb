import usocket as socket
import ujson as json

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
        self.address = address
        self.port = port
        self.active_socket = socket.socket()

        self.address_info = socket.getaddrinfo(self.address, self.port)
        self.address = self.address_info[0][-1]
        print("Bind address info:", self.address_info)

        self.active_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_socket.bind(self.address)
        self.active_socket.listen(5)

    #BACKEND SERVER METHODS
    def routes(self, routes={}):
        # set routes dict
        self.routes_dict = routes

    def router(self):
        if len(self.routes_dict) == 0:
            self.render('welcome.html')
        elif self.request_command:
            if (self.request_command, self.request_path) in self.routes_dict.keys():
                # check for valid route
                self.routes_dict[(self.request_command, self.request_path)]()
            elif '.' in self.request_path:
                #send file to client
                self.sendFile(self.request_path[1:])
        else:
            self.sendStatus(self.ERROR)

    def start(self, log=True):
        self.log = log
        print("uWeb server started! Connect to http://%s:%s/" % (self.address, self.port))
        if not self.log:
            print("Server logs are currently off.")
        while True:
            connection = self.active_socket.accept()
            self.client_socket = connection[0]
            self.client_address = connection[1]
            if self.log:
                print()
                print("Client address:", self.client_address)
                print("Client socket:", self.client_socket)
                print("Client Request:")
            self.request_line = self.client_socket.readline()
            if bool(self.request_line):  #check if request not empty
                if self.log:
                    print(self.request_line.decode().strip())
                self.resolveRequestLine()
                self.processRequest()
                self.router()
            self.client_socket.close()

    def render(self, html_file, variables=False, status=OK):
        # send HTML file to client
        try:
            rendered_content = self.readFile(html_file)
            if variables:
                for var_name, value in variables.items():
                    rendered_content = rendered_content.replace(b"{{%s}}" % var_name, str(value).encode())
            self.sendStatus(status)
            self.sendHeaders({'Content-Type': 'text/html'})
            self.sendBody(b'\n' + rendered_content)
        except Exception as e:
            if e.args[0] == 2:
                #catch file not found
                print('No such file: %s' % html_file)
                self.render('500.html', status=self.ERROR)

    def sendJSON(self, dict_to_send={}):
        # send JSON data to client
        self.sendStatus(self.OK)
        self.sendBody(json.dumps(dict_to_send))

    def sendFile(self, filename):
        # send file(ie: js, css) to client
        try:
            to_send = self.readFile(filename)
            self.sendStatus(self.OK)
            self.sendBody(to_send)
        except Exception as e:
            self.sendStatus(self.NOT_FOUND)
            print('File: %s was not found, so 404 was sent to client.' % file)

    def sendStatus(self, status_code):
        # send HTTP header w/ status to client
        response_line = b"HTTP/1.1 "
        self.send(response_line + status_code + b'\n')

    def sendHeaders(self, headers_dict={}):
        # send HTTP headers to client
        self.sendStatus(self.OK)
        for key, value in headers_dict.items():
            self.send(b"%s: %s\n" % (key.encode(), value.encode()))

    def sendBody(self, body_content):
        # send HTTP body content to client
        self.send(b'\n' + body_content)

    #HELPER METHODS
    def readFile(self, file):
        # read file and encode
        with open(file, 'r') as f:
            return ''.join(f.readlines()).encode()

    def send(self, content):
        # send to client @ socket-level
        self.client_socket.write(content)

    def processRequest(self):
        #process request from client --> extract headers + body
        raw_headers = []
        self.request_headers = {}

        #extract headers
        while True:
            h = self.client_socket.readline()
            if h == b"" or h == b"\r\n":
                break
            if self.log:
                print(h.decode().strip())
            raw_headers.append(h)
        for header in raw_headers:
            split_header = header.decode().strip().split(': ')
            self.request_headers[split_header[0]] = split_header[1]

        # extract body if its a POST request
        if self.request_command == self.POST:
            self.request_body = self.client_socket.read(int(self.request_headers['Content-Length'])).decode()
            if self.log:
                print(self.request_body)
            self.sendStatus(self.OK)

    def resolveRequestLine(self):
        # parse request line from client
        req_line = self.request_line.decode().strip().split(' ')
        if len(req_line) > 1:
            self.request_command = req_line[0]
            self.request_path = req_line[1]
            self.request_http_ver = req_line[2]
            return True
        else:
            return False

def loadJSON(string):
    # turn JSON string to dict
    return json.loads(string)
