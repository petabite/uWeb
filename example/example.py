import sys
import uasyncio
sys.path.append('../uWeb')
from uWeb import uWeb, loadJSON

server = uWeb("0.0.0.0", 8000)  #init uWeb object
global cancel
cancel = False

def home(): #render HTML page
    print('in home funciton')
    vars = {
        'name': 'MicroPython',
        'answer': (1+1)
    }
    await server.render('content.html', variables=vars)

def printTen():
    for i in range(10):
        print(i)
        await uasyncio.sleep(1)
        print(cancel)
        if cancel:
            return 
        
def cancell():
    global cancel
    cancel = True
    await uasyncio.sleep(0)

func = printTen
# def header(): #send headers to client
#     await server.sendStatus(server.OK)
#     await server.sendHeaders({
#         'header1': 'one',
#         'header2': 'two',
#         'header3': 'three',
#     })

# def post(): #print JSON body from client
#     print(loadJSON(server.request_body).items())

# def jsonn(): #send JSON to client
#     await server.sendJSON({'status':'okkk'})

#configure routes
server.routes(({
    (uWeb.GET, "/"): home,
    (uWeb.GET, "/ten"): printTen,
    (uWeb.GET, "/cancel"): cancell
    # (uWeb.POST, "/post"): post,
    # (uWeb.GET, "/json"): jsonn,
    # (uWeb.GET, "/header"): header
}))

#start server
server.start()
