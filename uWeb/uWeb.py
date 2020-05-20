import usocket as socket
import ujson as json
import gc
import network
import sys
import uasyncio

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

    MIME_TYPES = {
        'css': 'text/css',
        'html': 'text/html',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'js': 'text/javascript',
        'json': 'application/json',
        'rtf': 'application/rtf',
        'svg': 'image/svg+xml'
    }

    def __init__(self, address, port):
        #configure socket
        self.address = address
        self.port = port
        # self.active_socket = socket.socket()

        # self.address_info = socket.getaddrinfo(self.address, self.port)
        # self.address = self.address_info[0][-1]
        # print("Bind address info:", self.address_info[0][4])
        self.setSupportedFileTypes()
        self.routes() #init empty routes_dict
        # self.active_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.active_socket.bind(self.address)
        # self.active_socket.listen(5)

    #BACKEND SERVER METHODS
    def routes(self, routes={}):
        # set routes dict
        self.routes_dict = routes

    def router(self, writer):
        if len(self.routes_dict) == 0:
            await self.render('welcome.html')
        elif self.request_command:
            if (self.request_command, self.request_path) in self.routes_dict.keys():
                # check for valid route
                # try:
                loop = uasyncio.get_event_loop()
                loop.create_task(self.routes_dict[(self.request_command, self.request_path)]())
                # except TypeError:
                # await self.routes_dict[(self.request_command, self.request_path)]()
            elif ('.' in self.request_path):
                #send file to client
                await self.sendFile(self.request_path[1:])
            else:
                await self.render('404.html', layout=None, status=self.NOT_FOUND)
        else:
            await self.render('505.html', layout=None, status=self.ERROR)
        await writer.aclose()
        

    def start(self, log=True):
        self.log = log
        loop = uasyncio.get_event_loop()
        loop.create_task(uasyncio.start_server(self.serverRoutine, self.address, self.port)) # Schedule server loop
        loop.run_forever()

    def serverRoutine(self, reader, writer):
        # TODO: uncomment on release print("uWeb server started! Connect to http://%s:%s/" % (self.address, self.port))
        if not self.log:
            print("Server logs are currently off.")
        self.reader = reader
        self.writer = writer
        self.request = yield from reader.read()
        print()
        if bool(self.request):  #check if request not empty
            if self.log:
                print(self.request.decode().strip())
            self.processRequest()
            await self.router(writer)

        # self.send(b'HTTP/1.0 200 OK\r\n')
        # self.send(b'adsf')
        # await uasyncio.sleep(0)
        # while True:
        #     try:
                # connection = self.active_socket.accept()
                # self.client_socket = connection[0]
                # self.client_address = connection[1]
                # if self.log:
                    # print("Client address:", self.client_address)
                    # print("Client socket:", self.client_socket)
                    # print("Client Request:")
                # self.request_line = self.client_socket.readline()
                # if bool(self.request_line):  #check if request not empty
                #     if self.log:
                #         print(self.request_line.decode().strip())
                #     self.resolveRequestLine()
                #     self.processRequest()
                #     self.router()
                # self.client_socket.close()
            # except Exception as e:
            #     sys.print_exception(e)

    def render(self, html_file, layout='layout.html', variables=False, status=OK):
        # send HTML file to client
        print('in render funciton')
        try:
            if layout:
                # layout rendering
                file = layout
                with open(layout, 'r') as f:
                    gc.collect()
                    await self.sendStatus(status)
                    await self.sendHeaders({'Content-Type': 'text/html'})
                    await self.send(b'\n')
                    for line in f:
                        if '{{yield}}' in line:
                            splitted = line.split('{{yield}}')
                            await self.send(splitted[0].encode())
                            with open(html_file, 'r') as f:
                                for line in f:
                                    if variables:
                                        for var_name, value in variables.items():
                                            line = line.replace("{{%s}}" % var_name, str(value))
                                    await self.send(line.encode())
                            await self.send(splitted[1].encode())
                        else: 
                            await self.send(line.encode())
            else:
                # no layout rendering
                gc.collect()
                await self.sendStatus(status)
                await self.sendHeaders({'Content-Type': 'text/html'})
                await self.send(b'\n')
                file = html_file
                with open(html_file, 'r') as f:
                    for line in f:
                        if variables:
                            for var_name, value in variables.items():
                                line = line.replace("{{%s}}" % var_name, str(value))
                        await self.send(line.encode())
            await self.send(b'\n\n')
        except Exception as e:
            if e.args[0] == 2:
                #catch file not found
                print('No such file: %s' % file)
                await self.render('500.html', layout=None, status=self.ERROR)
            else:
                sys.print_exception(e)
        # uasyncio.sleep(0)

    def sendJSON(self, dict_to_send={}):
        # send JSON data to client
        await self.sendStatus(self.OK)
        await self.sendHeaders({'Content-Type': 'application/json'})
        await self.sendBody(json.dumps(dict_to_send))

    def sendFile(self, filename):
        # send file(ie: js, css) to client
        name, extension = filename.split('.')
        try:
            if extension in self.supported_file_types:
                # check if included in allowed file types
                with open(filename, 'r') as f:
                    await self.sendStatus(self.OK)
                    if extension in self.MIME_TYPES.keys():
                        await self.sendHeaders({'Content-Type': self.MIME_TYPES[extension]}) # send content type
                    await self.send(b'\n')
                    for line in f:
                        await self.send(line.encode())
                await self.send(b'\n\n')
            else:
                await self.sendStatus(self.ERROR)
                print('File: %s is not an allowed file' % filename)
        except Exception as e:
            await self.sendStatus(self.NOT_FOUND)
            print('File: %s was not found, so 404 was sent to client.' % filename)

    def sendStatus(self, status_code):
        # send HTTP header w/ status to client
        response_line = b"HTTP/1.1 "
        await self.send(response_line + status_code + b'\n')

    def sendHeaders(self, headers_dict={}):
        # send HTTP headers to client
        # self.sendStatus(self.OK)
        for key, value in headers_dict.items():
            await self.send(b"%s: %s\n" % (key.encode(), value.encode()))

    def sendBody(self, body_content):
        # send HTTP body content to client
        await self.send(b'\n' + body_content + b'\n\n')

    def setSupportedFileTypes(self, file_types = ['js', 'css']):
        #set allowed file types to be sent if requested
        self.supported_file_types = file_types

    #HELPER METHODS
    def readFile(self, file):
        # read file and encode
        try:
            with open(file, 'r') as f:
                return ''.join(f.readlines()).encode()
        except Exception as e:
            print(e)

    def send(self, content):
        # send to client @ socket-level
        print('sending: ', content)
        await self.writer.awrite(content)

    def processRequest(self):
        #process request from client --> extract request line + headers + body
        self.request_headers = {}

        # parse request line and headers from client
        request_line, rest_of_request = self.request.split(b'\r\n', 1)

        #extract request line
        request_line = request_line.decode().strip().split(' ')
        if len(request_line) > 1:
            self.request_command = request_line[0]
            self.request_path = request_line[1]
            self.request_http_ver = request_line[2]


        raw_headers, body = rest_of_request.split(b'\r\n\r\n', 1)
        raw_headers = raw_headers.split(b'\r\n')
        for header in raw_headers:
            split_header = header.decode().strip().split(': ')
            self.request_headers[split_header[0]] = split_header[1]

        print("Headers: ", self.request_headers)

        # extract body if its a POST request and send OK status
        if self.request_command == self.POST:
            self.request_body = body.decode()
            if self.log:
                print("Body: ", self.request_body)
            self.sendStatus(self.OK)        

def loadJSON(string):
    # turn JSON string to dict
    return json.loads(string)
