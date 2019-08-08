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

        #output = ""
        #output += "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
        keys = red.keys("*Name*")
        matches = []
        pattern = re.compile(".*[A-Za-z]([0-9]+)")
        output = []
        max = None
        for key in keys:
            value = red.mget(key)[0]
            if str(name).lower() in str(value).lower():
                match = pattern.match(str(key)).groups()[0]
                matches.append(match)
        for match in matches:
            row = {}
            keys = red.keys("*[A-Za-z]%s" % match)
            keys.sort()
            values = red.mget(keys)
            del_string = len(match)
            for i in range(len(keys)):
                row[str(keys[i][:-del_string])] = values[i]
                output.append(row)

        tmpl = env.get_template("results.html")
        return tmpl.render(data=output)

class BhavCopyPage(object):

    @cherrypy.expose
    def index(self):
        bhavcopy.download()
        red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

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
        output = []
        #output += "<b>" + "Date: " + bhavcopy.fname[2:4] + "-" + bhavcopy.fname[4:6] + "-" + bhavcopy.fname[6:8] + "</b><br /><br />"
        #serial = 1
        for index in results:
            row = {}
            #output += "<b>" + str(serial) + ") </b>"
            #serial += 1
            keys = red.keys("*[A-Za-z]%s" % index)
            keys.sort()
            values = red.mget(keys)
            del_string = len(str(index))
            for i in range(len(keys)):
                row[str(keys[i][:-del_string])] = str(values[i])
            output.append(row)
        tmpl = env.get_template('results.html')
        return tmpl.render(data=output)

root = HomePage()
root.bhavcopy = BhavCopyPage()

if __name__ == '__main__':
    bhavcopy = BhavCopy()
    cherrypy.quickstart(root, "/", config=config)
