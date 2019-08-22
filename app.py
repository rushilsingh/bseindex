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
    if fnc is None:
        return None
    header, table_header = reload()
    output = fnc(arg, **kw)
    return {"output": output, "header": header, "table_header": table_header}

def render(template, fnc=None, arg=None, **kw):
    return env.get_template(template).render(data=process(fnc, arg, **kw))

class HomePage(object):

    @staticmethod
    @cherrypy.expose
    def index():
        return render("index.html")

    @staticmethod
    @cherrypy.expose()
    def search(name):
        return render("results.html", search, name)

    @staticmethod
    @cherrypy.expose
    def rank(number):

        return render("results.html", rank, number, top=bhavcopy.top)

class BhavCopyPage(object):

    @staticmethod
    @cherrypy.expose
    def index():
        return render("results.html", search, "", full=True)

root = HomePage()
root.bhavcopy = BhavCopyPage()

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    cherrypy.quickstart(root, "/", config=config)
