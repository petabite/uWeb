import usocket as socket

class uWeb:

    def __init__(self):

        self.active_socket = socket.socket()

        self.address_info = socket.getaddrinfo("0.0.0.0", 8080)
        self.address = self.address_info[0][-1]
        print("Bind address info:", self.address_info)

        self.active_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_socket.bind(self.address)
        self.active_socket.listen(5)

    def start(self):
        print("Listening, connect your browser to http://<this_host>:8080/")

        counter = 0
        while True:
            connection = self.active_socket.accept()
            self.client_socket = connection[0]
            self.client_address = connection[1]
            print("Client address:", self.client_address)
            print("Client socket:", self.client_socket)

            print("Client Request:")
            request_line = self.client_socket.readline()
            print(request_line)
            while True:
                h = self.client_socket.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)
            print('after req')

            self.render('content.html', {"counter":counter})
            self.client_socket.close()

            counter += 1
            print()

    def render(self, html, variables):
        rendered_content = content
        for var_name, value in variables.items():
            rendered_content = rendered_content.replace(b"{{%s}}" % var_name, str(value).encode())

        self.client_socket.write(rendered_content)

server = uWeb()
server.start()
