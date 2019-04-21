try:
    import usocket as socket
except:
    import socket


CONTENT = b"""\
HTTP/1.0 200 OK

<h1>Hello #%d from MicroPython!</h1>
"""

def main(micropython_optimize=False):
    s = socket.socket()

    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        print("Request:")
        req = client_sock.readline()
        print(req)
        print('after req')
        while True:
            h = client_sock.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
        client_sock.write(CONTENT % counter)

        client_sock.close()

        counter += 1
        print()


main()
