<h1>μWeb (a.k.a microWeb)</h1>
<h5>Super simple web server for wifi-based micro-controllers that support MicroPython (ie. NodeMCU ESP8266)</h5>

-------

# TABLE OF CONTENTS
- [TABLE OF CONTENTS](#table-of-contents)
- [FEATURES](#features)
- [REQUIREMENTS](#requirements)
- [INSTALLATION](#installation)
- [QUICK START](#quick-start)
    - [Template Rendering](#template-rendering)
    - [Layout Rendering](#layout-rendering)
- [DOCUMENTATION](#documentation)
  - [Objects](#objects)
    - [`uWeb.uWeb(address, port)`](#uwebuwebaddress-port)
          - [Description](#description)
          - [Parameters](#parameters)
  - [Attributes](#attributes)
  - [Methods](#methods)
  - [`uWeb.routes(routes={})`](#uwebroutesroutes)
          - [Description](#description-1)
          - [Parameters](#parameters-1)
  - [`uWeb.start(log=True)`](#uwebstartlogtrue)
          - [Description](#description-2)
          - [Parameters](#parameters-2)
  - [`uWeb.render(html_file, layout='layout.html', variables=False, status=OK)`](#uwebrenderhtmlfile-layoutlayouthtml-variablesfalse-statusok)
          - [Description](#description-3)
          - [Parameters](#parameters-3)
  - [`uWeb.sendJSON(dict_to_send={})`](#uwebsendjsondicttosend)
          - [Description](#description-4)
          - [Parameters](#parameters-4)
  - [`uWeb.sendFile(filename)`](#uwebsendfilefilename)
          - [Description](#description-5)
          - [Parameters](#parameters-5)
  - [`uWeb.sendStatus(status_code)`](#uwebsendstatusstatuscode)
          - [Description](#description-6)
          - [Parameters](#parameters-6)
  - [`uWeb.sendHeaders(headers_dict={})`](#uwebsendheadersheadersdict)
          - [Description](#description-7)
          - [Parameters](#parameters-7)
  - [`uWeb.sendBody(body_content)`](#uwebsendbodybodycontent)
          - [Description](#description-8)
          - [Parameters](#parameters-8)
  - [`uWeb.setSupportedFileTypes(file_types = ['js', 'css'])`](#uwebsetsupportedfiletypesfiletypes--js-css)
          - [Description](#description-9)
          - [Parameters](#parameters-9)
  - [Helpers](#helpers)
  - [`uWeb.router()`](#uwebrouter)
          - [Description](#description-10)
  - [`uWeb.readFile(file)`](#uwebreadfilefile)
          - [Description](#description-11)
          - [Parameters](#parameters-10)
          - [Returns](#returns)
  - [`uWeb.send(content)`](#uwebsendcontent)
          - [Description](#description-12)
          - [Parameters](#parameters-11)
  - [`uWeb.processRequest()`](#uwebprocessrequest)
          - [Description](#description-13)
  - [`uWeb.resolveRequestLine()`](#uwebresolverequestline)
          - [Description](#description-14)
          - [Returns](#returns-1)
  - [`loadJSON(string)`](#loadjsonstring)
          - [Description](#description-15)
          - [Parameters](#parameters-12)
  - [Constants](#constants)
        - [HTTP Methods](#http-methods)
        - [HTTP Status Codes](#http-status-codes)

# FEATURES
  - Simple URL routing to actions
  - Render templates with layouts to the client
  - Super simple HTML templating
  - HTTP request parsing
  - Send files and json to client
  - Parse headers and body from client

# REQUIREMENTS
  - [Microcontroller](https://github.com/micropython/micropython/wiki/Boards-Summary) that supports micropython(such as NodeMCU ESP8266)
  - USB cable(possibly)
  - Wi-Fi connection

**MicroPython Libraries:**
  - ujson
  - usocket

# INSTALLATION
  1. Install micropython on your board of choice([ESP8266 installation](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro))
  1. Copy the μWeb project files to your board over the web using [MicroPython's WebREPL](https://github.com/micropython/webrepl) or through a serial connection with [Adafruit's ampy](https://github.com/pycampers/ampy)
  1. If your version of MicroPython does not come with ujson or usocket precompiled, copy them from [micropython-lib](https://github.com/micropython/micropython-lib)
  1. Along with the μWeb project files, make sure you have a boot.py for the initial setup of your board(ie: connecting to wifi) and main.py for the main μWeb code.
  1. Power your board and enjoy!

**No MicroPython board? No problem!**

You can run uWeb with the MicroPython unix port
  1. Build the unix MicroPython port ([here](https://github.com/micropython/micropython/wiki/Getting-Started#debian-ubuntu-mint-and-variants)) or get the prebuild executable ([here](https://github.com/petabite/uWeb/blob/master/bin/micropython?raw=true))
  2. Run `micropython example.py` in your console.

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

- μWeb comes loaded with a simple template rendering system that can render HTML with python variables.
- To replace a variable in the HTML template, surround the variable name with { {  } }. Then, render the template with the variables parameter.

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

### Layout Rendering

- Template rendering can be combined with layout rendering so that templates can share the same layout
- The default layout is `layout.html`
- Specify a specific layout to render your template with using the `layout` argument in the `render` function
- Use `{{yield}}` to specify where in the layout you want the content to render

Using the example from above:

**content.html**
``` html
<h1>Hello from {{name}}!</h1>
<h3>1 + 1 = {{answer}}</h3>
```

**cool-layout.html**
``` html
<head>
    <title>cool site</title>
</head>
<body>
    <h1>this is a cool layout dude</h1>
    {{yield}}
</body>
```

**example.py**
```python
vars = {
      'name': 'MicroPython',
      'answer': (1+1)
  }
  server.render('content.html', layout='cool-layout.html', variables=vars) # if you are using layout.html, the layout argument may be left out
```

**will render as:**

``` html
<head>
    <title>cool site</title>
</head>
<body>
    <h1>this is a cool layout dude</h1>
    <h1>Hello from MicroPython!</h1>
    <h3>1 + 1 = 2</h3>
</body>
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

     Example:
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

## `uWeb.render(html_file, layout='layout.html', variables=False, status=OK)`

   ###### Description
   Send HTML file to client's browser
   ###### Parameters
  - html_file - (str) file name of html file to render
  - layout - (str) layout to render `html_file` with(see [Layout Rendering](#layout-rendering))
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

## `uWeb.setSupportedFileTypes(file_types = ['js', 'css'])`

  ###### Description
  - Specify the file extensions to be allowed to be sent to the client if it is requested. Use to protect your backend of your Microcontroller.
  - When allowing additional files, don't forget to include 'js' and 'css' in the list as well
  - This only applies to GET requests. You can still manually send files of any extension with [sendFile()](#uwebsendfilefilename)
  - NOTE: Be careful when allowing file types such as .py because the client can request /boot.py and may exposed sensitive info such as your wi-fi password if you have it set there.
  ###### Parameters
  - file_types - (list) file extensions to whitelist. Default: .js and .css

----

## Helpers

## `uWeb.router()`

   ###### Description
   Handles requests and run actions when a route matches

----

## `uWeb.readFile(file)`

  ###### Description
  Read and encode a file. Depending on your hardware, this method may raise a memory allocation error if the file is larger than the available memory.
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
