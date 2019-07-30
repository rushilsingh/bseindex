import cherrypy
from bhavcopy import BhavCopy
import cherrys
import redis
cherrypy.lib.sessions.RedisSession = cherrys.RedisSession


config = {
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'redis',
    'tools.sessions.host' : '127.0.0.1',
    'tools.sessions.port' : 6379,
    'tools.sessions.db' : 0,
    'tools.sessions.password' : None
    }


class App(object):
    @cherrypy.expose
    def index(self):
        red = redis.Redis("localhost", 6379)
        output = ""
        index = 1
        while True:
            keys = red.keys('*[A-Za-z]%s' % (index))
            vals = red.mget(keys)
            if len(vals) == 0:
                break
            kv = zip(keys, vals)
            for pair in kv:
                output += pair[0] + " : " +pair[1] + " , "
            output += "<break />"
            open_index = red.keys('Open%s' % index)
            open_index = red.mget(open_index[0])[0]
            close_index = red.keys('Close%s' % index)
            close_index = red.mget(close_index[0])[0]
            open_index = float(open_index)
            diff = float(open_index) - float(close_index)

            index += 1
        return output




if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()
    cherrypy.quickstart(App())

