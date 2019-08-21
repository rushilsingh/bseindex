import json
import re
import cherrypy
from bhavcopy import BhavCopy
import redis
import os
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))

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


class HomePage(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(data=None)


    @cherrypy.expose()
    def search(self, name):
        
        bhavcopy.download()
        fname = bhavcopy.fname

        header = ""
        header += "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        
        #red = redis.Redis()
        if name == "":
            data = {"header": header, "output": {}}
            return tmpl.render(data=data)
        
        output = []
        values = []
        search = "*" + name.upper()  + "*"
        cursor = 0
        while True:
            cursor, value = red.hscan("Names", cursor, search, 1000)
            if value != {}:
                for key in value:
                    entry = json.loads(value[key])
                    output.append(entry)
            if cursor == 0:
                break
        
        tmpl = env.get_template("results.html")
        data = {"header": header, "output": output}
        return tmpl.render(data=data)

    @cherrypy.expose
    def rank(self, number):
        bhavcopy.download()
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
        header = "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        data = {"header": header, "output": output}
        
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

class BhavCopyPage(object):

    @cherrypy.expose
    def index(self):
        bhavcopy.download()
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        #red = redis.Redis() 
        top = bhavcopy.top[:10] 
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
        header = "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        data = {"header": header, "output": output}
        
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

root = HomePage()
root.bhavcopy = BhavCopyPage()

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    cherrypy.quickstart(root, "/", config=config)
