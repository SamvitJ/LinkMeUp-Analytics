
import pymongo
import json
from bottle import Bottle, request, response, run

app = Bottle()

# this is the handler for the default path of the web server

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/', method=['OPTIONS', 'GET'])
def index():
    
    # connect to mongoDB
    connection = pymongo.MongoClient('localhost', 27017)

    # attach to test database
    db = connection.test

    # get handle for users collection
    users = db.users

    # return all users with valid location coordinates
    all_users = users.find( { "$and": [{"latitude" : {"$exists": True}}, {"longitude": {"$exists": True}}] })

    # create array of locations
    location_list = []

    for user in all_users:

        country = user.get('country', None)
        state = user.get('state', None)
        city = user.get('city', None)

        lat = user.get('latitude', None)
        lng = user.get('longitude', None)
        
        if country is None:
            continue

        if city is None:
            location_list.append([country, lat, lng])

        else:
            location_list.append(["%s, %s" % (city, state), lat, lng])


    # city_list = users.distinct("city")

    return json.dumps({"locations": location_list})


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--host", dest="host", default="localhost",
                      help="hostname or ip address", metavar="host")
    parser.add_option("--port", dest="port", default=8080,
                      help="port number", metavar="port")
    run(app, host='localhost', port=8082)