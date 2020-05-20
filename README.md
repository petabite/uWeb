<h1>μWeb (a.k.a microWeb)</h1>
<h5>Super simple web server for wifi-based micro-controllers that support MicroPython (ie. NodeMCU ESP8266)</h5>

---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Changelog](#changelog)
- [Requirements](#requirements)
- [uWeb vs. uWeb-uasyncio](#uweb-vs-uweb-uasyncio)
- [Installation](#installation)
- [Quick Start](#quick-start)
    - [Example application using μWeb](#example-application-using-%ce%bcweb)
    - [Example application using uWeb-uasyncio](#example-application-using-uweb-uasyncio)
- [Using uWeb-uasyncio](#using-uweb-uasyncio)
- [Template Rendering](#template-rendering)
- [Layout Rendering](#layout-rendering)
- [Documentation](#documentation)

# Features

- Simple URL routing to actions
- Render templates with layouts to the client
- Super simple HTML templating
- HTTP request parsing
- Send files and json to client
- Parse headers and body from client
- Optional asynchronous version (based on uasyncio)

# Changelog

<ins>**uWeb**</ins>

**v1.1 - 5/19/20**

- layout rendering
- send appropriate Content-Type headers when sending files
- version attribute

**v1.0 - 7/6/19**

- First release!

<ins>**uWeb-uasyncio**</ins>

**v1.0 - //20**

- First release!

# Requirements

- [Microcontroller](https://github.com/micropython/micropython/wiki/Boards-Summary) that supports micropython(such as NodeMCU ESP8266)
- USB cable(possibly)
- Wi-Fi connection

**MicroPython Libraries:**

- ujson
- usocket
- uasyncio(for uasyncio version)

# uWeb vs. uWeb-uasyncio

This repo contains both uWeb and uWeb-uasyncio. Both versions have their own use cases

|     ;-;     |                                         uWeb                                          |                                                      uWeb-uasyncio                                                      |
| :---------: | :-----------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------: |
| concurrency |                    not concurrent, uses usocket(blocking sockets)                     |                                supports concurrency, uses uasyncio(non-blocking sockets)                                |
| when to use |             when you need a simple web server to serve HTML or send data              |       when endpoints call functions that take time to run and having the server respond to requests is important        |
|  use cases  | simple API that serves static files or sends some JSON data(concurrency not required) | app where a request to an endpoint invokes a function that sleeps for some time but still responds to incoming requests |

**TLDR; uWeb can be used when concurrency is not important. uWeb-uasyncio can be used when concurrency is important

# Installation

1. Install micropython on your board of choice([ESP8266 installation](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro))
2. Copy the μWeb project files to your board over the web using [MicroPython's WebREPL](https://github.com/micropython/webrepl) or through a serial connection with [Adafruit's ampy](https://github.com/pycampers/ampy)
     - chose either `uWeb.py` or `uWeb_uasyncio.py` depending on your needs
3. If your version of MicroPython does not come with ujson, usocket or uasyncio(if needed) precompiled, copy them from [micropython-lib](https://github.com/micropython/micropython-lib)
4. Along with the μWeb project files, make sure you have a boot.py for the initial setup of your board(ie: connecting to wifi) and main.py for the main μWeb code.
5. Power up your board and enjoy!

**No MicroPython board? No problem!**

You can run uWeb with the MicroPython unix port

1. Build the unix MicroPython port ([here](https://github.com/micropython/micropython/wiki/Getting-Started#debian-ubuntu-mint-and-variants)) or get the prebuild executable ([here](https://github.com/petabite/uWeb/blob/master/bin/micropython?raw=true))
2. Run `micropython uWeb_example.py` or `micropython uWeb_uasyncio_example.py` in your console.

# Quick Start

### Example application using μWeb

```python
from uWeb import uWeb, loadJSON

server = uWeb("0.0.0.0", 8000)  #init uWeb object

def home(): #render HTML page
    vars = {
        'name': 'MicroPython',
        'answer': (1+1)
    }
    server.render('content.html', variables=vars)

def header(): #send headers to client
    server.sendStatus(server.OK)
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

### Example application using uWeb-uasyncio

```python
import uasyncio
from uWeb_uasyncio import uWeb_uasyncio as uWeb
from uWeb_uasyncio import loadJSON

server = uWeb("0.0.0.0", 8000)  #init uWeb object

def home(): #render HTML page
    vars = {
        'name': 'MicroPython',
        'answer': (1+1)
    }
    await server.render('content.html', variables=vars)

def printTen(): # counts to ten while still accepting incoming requests
    await server.sendStatus(server.OK)
    for i in range(10):
        print(i)
        await uasyncio.sleep(1)

def header(): #send headers to client
    await server.sendStatus(server.OK)
    await server.sendHeaders({
        'header1': 'one',
        'header2': 'two',
        'header3': 'three',
    })

def post(): #print JSON body from client
    print('Payload: ', loadJSON(server.request_body))
    await uasyncio.sleep(0)

def jsonn(): #send JSON to client
    await server.sendJSON({'status':'okkk'})

#configure routes
server.routes(({
    (uWeb.GET, "/"): home,
    (uWeb.GET, "/ten"): printTen,
    (uWeb.POST, "/post"): post,
    (uWeb.GET, "/json"): jsonn,
    (uWeb.GET, "/header"): header
}))

#start server
server.start()
```

# Using uWeb-uasyncio

- when configuring routes, endpoint functions are treated as asynchronous so they must have an `await` statement in its body
- usually uWeb class methods can be preceded with `await`
- when using other functions that aren't `await`able, `await uasyncio.sleep(0)` can be used (as seen in the example)
- more info about using `uasyncio`: [uasyncio docs](https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md)

# Template Rendering

- μWeb comes loaded with a simple template rendering system that can render HTML with python variables.
- To replace a variable in the HTML template, surround the variable name with `{{ }}`. Then, render the template with the variables argument.

Example:

**content.html**

```html
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

```html
<h1>Hello from MicroPython!</h1>
<h3>1 + 1 = 2</h3>
```

# Layout Rendering

- Template rendering can be combined with layout rendering so that templates can share the same layout
- The default layout is `layout.html`
- Specify a specific layout to render your template with using the `layout` argument in the `render` function
- Use `{{yield}}` to specify where in the layout you want the content to render

Using the example from above:

**content.html**

```html
<h1>Hello from {{name}}!</h1>
<h3>1 + 1 = {{answer}}</h3>
```

**cool-layout.html**

```html
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

```html
<head>
  <title>cool site</title>
</head>
<body>
  <h1>this is a cool layout dude</h1>
  <h1>Hello from MicroPython!</h1>
  <h3>1 + 1 = 2</h3>
</body>
```
# Documentation
- [uWeb](https://github.com/petabite/uWeb/blob/master/docs/uWeb.md)
- [uWeb-uasyncio](https://github.com/petabite/uWeb/blob/master/docs/uWeb-uasyncio.md)