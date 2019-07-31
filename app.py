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
    }
}


class HomePage(object):
    @cherrypy.expose
    def index(self):
        output = "<a href=\"/bhavcopy/\">Latest Bhavcopy Data</a>"
        tmpl = env.get_template('index.html')
        return tmpl.render(data=output)

class BhavCopyPage(object):
    
    @cherrypy.expose
    def index(self):
        bhavcopy.download()
        red = redis.from_url(os.environ.get("REDIS_URL"))

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
        output += "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        serial = 1
        for index in results:
            output += "<b>" + str(serial) + ")"
            serial += 1
            keys = red.keys("*[A-Za-z]%s" % index)
            values = red.mget(keys)
            del_string = len(str(index))
            for i in range(len(keys)):
                output += str(keys[i][:-del_string]) + "</b>" + " : " + str(values[i]) + " , "
            output = output[:-len(" , ")]
            output += "<br /><br />"
        tmpl = env.get_template('index.html')
        return tmpl.render(data=output)

root = HomePage()
root.bhavcopy = BhavCopyPage()
if __name__ == '__main__':
    bhavcopy = BhavCopy()
    cherrypy.quickstart(root, "/", config=config)
