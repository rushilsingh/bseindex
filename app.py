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
        action = "search"
        tmpl = env.get_template('index.html')
        return tmpl.render(data=action)


    @cherrypy.expose()
    def search(self, name):
        
        bhavcopy.download()
        fname = bhavcopy.fname

        header = ""
        header += "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        output = []
        values = []
        search = "*" + name  + "*"
        cursor = 0
        while True:
            cursor, value = red.hscan("Names", cursor, search, 1000)
            if cursor == 0:
                break
            if value:
                import pickle
                values.append(pickle.loads(value).decode(errors='replace'))
        output = values

        tmpl = env.get_template("results.html")
        data = {"header": header, "output": output}
        return tmpl.render(data=data)

class BhavCopyPage(object):

    @cherrypy.expose
    def index(self):
        bhavcopy.download()
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        top = bhavcopy.top 
        print(top)
        output = []
        cursor = 0
        for search in top:
            print(search)
            while True:
                cursor, value = red.hscan("Diffs", cursor, search, 1000)
                if cursor == 0:
                    break
                if value:
                    import pickle
                    output.append(pickle.loads(value).decode(errors='replace'))
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
