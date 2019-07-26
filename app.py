import cherrypy
from bhavcopy import BhavCopy


class App(object):
    @cherrypy.expose
    def index(self):
        return "Bhavcopy contents"


if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()

    cherrypy.quickstart(App())

