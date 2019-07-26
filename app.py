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
        keys = red.keys('*')
        vals = []
        for key in keys:
            type = red.type(key)
            if type == KV:
                val = red.get(key)
            if type == HASH:
                vals = red.hgetall(key)
            if type == ZSET:
                 vals = red.zrange(key, 0, -1)
        kv = zip(keys, vals)
        print kv
        return kv

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()
    cherrypy.quickstart(App())

