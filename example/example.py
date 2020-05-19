import sys
sys.path.append('../uWeb')
from uWeb import uWeb, loadJSON

server = uWeb("0.0.0.0", 8000)  #init uWeb object

def home(): #render HTML page
    print('in home funciton')
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
