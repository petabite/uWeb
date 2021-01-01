<h1> uWeb asyncio Documentation</h1>

**This is the documentation for uWeb-uasyncio. Click [here](https://github.com/petabite/uWeb/blob/master/docs/uWeb.md) if you're looking for the docs for uWeb**

## Table of Contents
- [Table of Contents](#table-of-contents)
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
- [`uWeb.router(reader, writer)`](#uwebrouterreader-writer)
        - [Description](#description-10)
        - [Parameters](#parameters-10)
- [`uWeb.readFile(file)`](#uwebreadfilefile)
        - [Description](#description-11)
        - [Parameters](#parameters-11)
        - [Returns](#returns)
- [`uWeb.send(content)`](#uwebsendcontent)
        - [Description](#description-12)
        - [Parameters](#parameters-12)
- [`uWeb.processRequest()`](#uwebprocessrequest)
        - [Description](#description-13)
- [`loadJSON(string)`](#loadjsonstring)
        - [Description](#description-14)
        - [Parameters](#parameters-13)
        - [Returns](#returns-1)
- [Constants](#constants)
      - [HTTP Methods](#http-methods)
      - [HTTP Status Codes](#http-status-codes)
      - [MIME types](#mime-types)

## Objects
uWeb_uasyncio refered to as uWeb for simplicity

### `uWeb.uWeb(address, port)`

 ###### Description
Initialize a uWeb object by configuring socket to bind and listen to specified address and port.

  ###### Parameters
  - address - (str) address to listen on
  - port - (int) port to listen on

## Attributes

  - `uWeb.version` - (str) uWeb version
  - `uWeb.address` - address that is bound to
  - `uWeb.port` - (int) port that is bound to
  - `uWeb.reader` - (StreamReader) StreamReader passed by uasyncio start_server method
  - `uWeb.writer` - (StreamWriter) StreamWriter passed by uasyncio start_server method
  - `uWeb.routes_dict` - (dict) all routes
  - `uWeb.request` - (bytestr) raw request string from `uWeb.reader`
  - `uWeb.request_command` - (str) HTTP method of request(ie: POST, GET, PUT, etc)
  - `uWeb.request_path` - (str) requested path
  - `uWeb.request_http_ver` - (str) HTTP version of request
  - `uWeb.request_body` - (str) body of current request
  - `uWeb.request_headers` - (dict) headers of  current request

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
  - Send file to client along with its appropriate Content-Type header. This is automatically called depending on the path of the HTTP request. EX: if a .js is requested, uWeb will look for it and send it if it exists.
  - Add MIME types by appending to the `MIME_TYPES` dictionary
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

## `uWeb.router(reader, writer)`

   ###### Description
   Handles requests and run actions when a route matches
   ###### Parameters
   - reader - (StreamReader) StreamReader passed by uasyncio start_server method
   - writer - (StreamWriter) StreamWriter passed by uasyncio start_server method

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
   Process request from client by extracting request line to corresponding request variables, headers to request_headers and extract body to request_body if it is a POST request.

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

##### MIME types
  - 'css': 'text/css'
  - 'html': 'text/html'
  - 'jpeg': 'image/jpeg'
  - 'jpg': 'image/jpeg'
  - 'js': 'text/javascript'
  - 'json': 'application/json'
  - 'rtf': 'application/rtf'
  - 'svg': 'image/svg+xml'
