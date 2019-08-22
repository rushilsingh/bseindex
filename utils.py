import redis
import json
import os


def search(name, full=False):

    if full:
        search = "*"
    else:
        if name == "":
            data = {"header": header, "table_header": table_header, "output": {}}
            return data
        else:
            search = "*" + name.upper() +"*"
    output = []
    cursor = 0

    red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
    #red = redis.Redis()

    while True:
        cursor, value = red.hscan("Names", cursor, search, 1000)
        if value != {}:
            for key in value:
                entry = json.loads(value[key])
                output.append(entry)
        if cursor == 0:
            break

    return output

def rank(number, **kw):

    try:
        number = int(number)
        if number<0:
            raise ValueError
    except ValueError:
        return {"header": header, "table_header": table_header, "output":"Invalid input"}

    red = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
    #red = redis.Redis()
    top = kw.get("top", None)
    if top is None:
        return []
    top = top[:number]
    output = []
    cursor = 0
    entries = 0
    for search in top:
        while True:
            cursor, value = red.hscan("Diffs", cursor, search, 1000)
            if value != {}:
                for key in value:
                    entry = json.loads(value[key])
                    output.append(entry)
                    entries += 1
                    if entries >= 10:
                        break
            if cursor == 0:
                break
    return output
