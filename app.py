import json
import cherrypy
from bhavcopy import BhavCopy
import redis
import os
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'), autoescape=True)
table_header = ["Code", "Name", "Open", "Close", "High", "Low", "Change"]

config = {

    'global': {
'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },

    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    },
    '/favicon.ico': {
    'tools.staticfile.on': True,
    'tools.staticfile.filename': os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")
    }
}

def search(name, full=False):
    
    bhavcopy.download()
    header = "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8]
    if full:
        search = "*"
    else:
        if name == "":
            data = {"header": header, "table_header": table_header, "output": {}}
            return data
        else:
            search = "*" + name.upper() +"*"
    output = []
    cursor = 0

    red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
    #red = redis.Redis()

    while True:
        cursor, value = red.hscan("Names", cursor, search, 1000)
        if value != {}:
            for key in value:
                entry = json.loads(value[key])
                output.append(entry)
        if cursor == 0:
            break

    data = {"header": header, "table_header": table_header, "output": output}
    return data

def rank(number):
    
    bhavcopy.download()
    header = "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8]
    tmpl = env.get_template("results.html")
    try:
        number = int(number)
        if number<0:
            raise ValueError
    except ValueError:
        return {"header": header, "table_header": table_header, "output":"Invalid input"}

    red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
    #red = redis.Redis()
    top = bhavcopy.top[:number]
    output = []
    cursor = 0
    entries = 0
    for search in top:
        while True:
            cursor, value = red.hscan("Diffs", cursor, search, 1000)
            if value != {}:
                for key in value:
                    entry = json.loads(value[key])
                    output.append(entry)
                    entries += 1
                    if entries >= 10:
                        break
            if cursor == 0:
                break
    data = {"header": header, "table_header": table_header,  "output": output}
    return data

class HomePage(object):
    @cherrypy.expose
    def index(self):
        bhavcopy.download()
        tmpl = env.get_template('index.html')
        return tmpl.render()


    @cherrypy.expose()
    def search(self, name):
        data = search(name)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

    @cherrypy.expose
    def rank(self, number):

        data = rank(number)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

class BhavCopyPage(object):

    @cherrypy.expose
    def index(self):

        data = search("", full=True)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

root = HomePage()
root.bhavcopy = BhavCopyPage()

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    cherrypy.quickstart(root, "/", config=config)
