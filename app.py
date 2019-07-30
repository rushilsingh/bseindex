import cherrypy
from bhavcopy import BhavCopy
import redis
import os
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))




config = {


    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'redis',
    'tools.sessions.host' : '127.0.0.1',
    'tools.sessions.port' : 6379,
    'tools.sessions.db' : 0,
    'tools.sessions.password' : None

    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}


class App(object):
    @cherrypy.expose
    def index(self):
        red = redis.Redis("localhost", 6379)
        output = []
        dictionary = {}
        index = 1
        max = None
        while True:
            keys = red.keys('*Change%s' % (index))
            if len(keys) == 0:
                break
            key = keys[0]
            value = red.mget(key)[0]
            output.append(value)
            dictionary[index] = value
            index += 1
        output.sort()
        output.reverse()
        output = output[0:10]
        results = []
        index = 0
        for value in output:
            for key in dictionary:
                if dictionary[key] == value:
                    results.append(key)
                    break
        output = ""
        for index in results:
            keys = red.keys("*[A-Za-z]%s" % index)
            values = red.mget(keys)
            del_string = len(str(index))
            for i in range(len(keys)):
                output += str(keys[i][:-del_string]) + " : " + str(values[i]) + " , "
            output += "<br />"
        tmpl = env.get_template('index.html')
        return tmpl.render(data=output)








if __name__ == '__main__':
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()
    cherrypy.quickstart(App(), "/", config=config)

