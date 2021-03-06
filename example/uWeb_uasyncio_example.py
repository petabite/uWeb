import sys
import uasyncio
sys.path.append('../uWeb') # remove this if deploying to a board
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
