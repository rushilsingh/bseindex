import cherrypy
from bhavcopy import BhavCopy
import cherrys
cherrypy.lib.sessions.RedisSession = cherrys.RedisSession

config = {
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'redis',
    'tools.sessions.host' : '127.0.0.1',
    'tools.sessions.port' : 6379,
    'tools.sessions.db' : 0,
    'tools.sessions.password' : None
    }
cherrypy.config.update(config)


class App(object):
    @cherrypy.expose
    def index(self):
        return "Bhavcopy contents"


if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()

    cherrypy.quickstart(App())

