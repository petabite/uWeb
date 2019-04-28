# μWeb (a.k.a microWeb)
###### Super simple web server for wifi-based micro-controllers that support MicroPython (ie. NodeMCU ESP8266)

-------

# FEATURES
  - Simple URL routing to actions
  - Render templates to the client
  - Super simple HTML templating
  - HTTP request parsing
  - Send files and json to client
  - Parse headers and body from client

# REQUIREMENTS
  - [Microcontroller](https://github.com/micropython/micropython/wiki/Boards-Summary) that supports micropython(such as NodeMCU ESP8266)
  - USB cable(possibly)
  - Wi-Fi connection

##### MicroPython Libraries:
  - ujson
  - usocket

# INSTALLATION
  1. Install micropython on your board of choice([ESP8266 installation](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro))
  1. Copy the μWeb project files to your board over the web using [MicroPython's WebREPL](https://github.com/micropython/webrepl) or through a serial connection with [Adafruit's ampy](https://github.com/pycampers/ampy)
  1. If your version of MicroPython does not come with ujson or usocket precompiled, copy them from [micropython-lib](https://github.com/micropython/micropython-lib)
  1. Along with the μWeb project files, make sure you have a boot.py for the initial setup of your board(ie: connecting to wifi) and main.py for the main μWeb code.
  1. Power your board and enjoy!

###### No MicroPython board? No problem!

You can run uWeb with the MicroPython unix port
  1. Build the unix MicroPython port ([here](https://github.com/micropython/micropython/wiki/Getting-Started#debian-ubuntu-mint-and-variants)) or get the prebuild executable ([here](https://github.com/petabite/uWeb/blob/master/bin/micropython?raw=true))
  1. Run `micropython example.py` in your console.

# QUICK START

Example application using μWeb
``` python
from uWeb import uWeb, loadJSON

server = uWeb("0.0.0.0", 8080)  #init uWeb object

def home(): #render HTML page
    server.render('content.html')

def header(): #send headers to client
    server.sendHeaders({
        'header1': 'one',
        'header2': 'two',
        'header3': 'three',
    })

def post(): #print JSON body from client
    print(loadJSON(server.request_body).items())

def jsonn(): #send JSON to client
    server.sendJSON({'status':'okkk'})

#configure routes
server.routes(({
    (uWeb.GET, "/"): home,
    (uWeb.POST, "/post"): post,
    (uWeb.GET, "/json"): jsonn,
    (uWeb.GET, "/header"): header
}))

#start server
server.start()

```
### Template Rendering  

μWeb comes loaded with a simple template rendering system that can render HTML with python variables.

To replace a variable in the HTML template, surround the variable name with { {  } }. Then, render the template with the variables parameter.

Example:

**content.html**
``` html
<h1>Hello from {{name}}!</h1>
<h3>1 + 1 = {{answer}}</h3>
```

**example.py**
```python
vars = {
      'name': 'MicroPython',
      'answer': (1+1)
  }
  server.render('content.html', variables=vars)
```

**will render as:**

``` html
<h1>Hello from MicroPython!</h1>
<h3>1 + 1 = 2</h3>
```

# DOCUMENTATION

## Objects

### `uWeb.uWeb(address, port)`

 ###### Description
Initialize a uWeb object by configuring socket to bind and listen to specified address and port.

  ###### Parameters
  - address - (str) address to listen on
  - port - (int) port to listen on

## Attributes

  - `uWeb.address` - address that is bound to
  - `uWeb.port` - (int) port that is bound to
  - `uWeb.routes_dict` - (dict) all routes
  - `uWeb.request_command` - (str) HTTP method of request(ie: POST, GET, PUT, etc)
  - `uWeb.request_path` - (str) requested path
  - `uWeb.request_http_ver` - (str) HTTP version of request
  - `uWeb.request_body` - (str) body of current request
  - `uWeb.request_headers` - (dict) headers of  current request
  - `uWeb.client_socket` - (socket) socket object of active socket
  - `uWeb.client_address` - address of client

## Methods
## `uWeb.routes(routes={})`

   ###### Description
   Use this method to specify routes for the app.
   ###### Parameters
   - routes - (dict) dictionary containing routes in format:
   ``` python
   {
       (HTTP_METHOD, PATH): ACTION,
       (HTTP_METHOD, PATH): ACTION
   }
   ```

      - HTTP_METHOD - method to listen for(see [Constants](#constants))
      - PATH - URL to listen for
      - ACTION - function to be run when route matches

     - Example:

     ``` python
     {
         (uWeb.GET, "/"): home,
         (uWeb.POST, "/post"): post,
         (uWeb.GET, "/json"): jsonn,
         (uWeb.GET, "/header"): header
     }
     ```
-----

## `uWeb.start(log=True)`

  ###### Description
  Start the server.
  ###### Parameters
  - log - (bool) default: True; toggle logging of client information and requests to console

-----

## `uWeb.render(html_file, variables=False, status=OK)`

   ###### Description
   Send HTML file to client's browser
   ###### Parameters
  - html_file - (str) file name of html file to render
  - variables - (dict) dictionary of variables to render html with(see [Template Rendering](#template-rendering)).  

    Example:

    ``` python
    {
      "variable_name_in_html": "replace_with_this",
      "another_one", (1 + 1)
    }
    ```

  - status - (str) HTTP status to send to client. Default: uWeb.OK(see [Constants](#constants))

-----

## `uWeb.sendJSON(dict_to_send={})`

  ###### Description
  Send JSON body to client.
  ###### Parameters
  - dict_to_send - (dict) dictionary with JSON data

----

## `uWeb.sendFile(filename)`

  ###### Description
  Send file such as .js or .css to client. This is automatically called depending on the path of the HTTP request. EX: if a .js is requested, uWeb will look for it and send it if it exists.
  ###### Parameters
  - filename - (str) name of file to send

----

## `uWeb.sendStatus(status_code)`

  ###### Description
  Send HTTP response header to client with specified status
  ###### Parameters
  - status_code - (str) HTTP status code(see [Constants](#constants))

----

## `uWeb.sendHeaders(headers_dict={})`

  ###### Description
  Send HTTP headers to client.
  ###### Parameters
  - headers_dict - (dict) dictionary containing header and values to be sent to client.
  Example:
  ```python
  {
        'header1': 'one',
        'header2': 'two',
        'header3': 'three',
  }
  ```

----

## `uWeb.sendBody(body_content)`

  ###### Description
  Send response body content to client
  ###### Parameters
  - body_content - (bytestring) body content to send

----

## Helpers

## `uWeb.router()`

   ###### Description
   Handles requests and run actions when a route matches

----

## `uWeb.readFile(file)`

  ###### Description
  Read and encode a file
  ###### Parameters
  - file - (str) filename of file to be read and encoded

  ###### Returns
  - (bytestring) encoded file

----

## `uWeb.send(content)`

   ###### Description
   Basic method to send bytestring to client
   ###### Parameters
  - content - (bytestring) content to send

----

## `uWeb.processRequest()`

   ###### Description
   Process request from client by extracting headers to request_headers and extract body to request_body if it is a POST request.

----

## `uWeb.resolveRequestLine()`

  ###### Description
  Parse request line from client. Sets: request_command, request_path, and request_http_ver
  ###### Returns
  - (bool) True: if a valid request_line; False: if request_line empty

----

## `loadJSON(string)`

   ###### Description
   Not part of uWeb class. Easy way to convert a request_body containing a JSON string to a dict

   ###### Parameters
  - string - (str) JSON string to convert to dictionary

    ###### Returns
  - (dict) dictionary with converted JSON

----

## Constants
##### HTTP Methods
  - uWeb.GET = 'GET'
  - uWeb.POST = 'POST'
  - uWeb.PUT = 'PUT'
  - uWeb.DELETE = 'DELETE'

##### HTTP Status Codes
  - uWeb.OK = b"200 OK"
  - uWeb.NOT_FOUND = b"404 Not Found"
  - uWeb.FOUND = b"302 Found"
  - uWeb.FORBIDDEN = b"403 Forbidden"
  - uWeb.BAD_REQUEST = b"400 Bad Request"
  - uWeb.ERROR = b"500 Internal Server Error"
