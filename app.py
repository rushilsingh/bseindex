import cherrypy
from bhavcopy import BhavCopy
import os
from jinja2 import Environment, FileSystemLoader
from utils import search, rank

env = Environment(loader=FileSystemLoader('html'), autoescape=True)

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

def reload():
    bhavcopy.download()
    fname = bhavcopy.fname
    header = "Date: " + fname[2:4] + "-" + fname[4:6] + "-" + fname[6:8]
    table_header = ["Code", "Name", "Open", "Close", "High", "Low", "Change"]
    return header, table_header

def process(fnc, arg, **kw):
    header, table_header = reload()
    output = fnc(arg, **kw)
    return {"output": output, "header": header, "table_header": table_header}
    
class HomePage(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()


    @cherrypy.expose()
    def search(self, name):
        data = process(search, name)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

    @cherrypy.expose
    def rank(self, number):
        
        data = process(rank, number, top=bhavcopy.top)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

class BhavCopyPage(object):

    @cherrypy.expose
    def index(self):
        data = process(search, "", full=True)
        tmpl = env.get_template("results.html")
        return tmpl.render(data=data)

root = HomePage()
root.bhavcopy = BhavCopyPage()

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    cherrypy.quickstart(root, "/", config=config)
