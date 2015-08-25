
import pymongo
import json
import datetime
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

    # reference time (used for time code)
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    # print "%s %s" % (one_day_ago, one_week_ago)

    # create array of locations
    location_list = []

    for user in all_users:

        # determine time code
        createdAt = user.get('createdAt', None)
        time_code = 0

        if createdAt > one_hour_ago.isoformat():
            time_code = 3

        elif createdAt > one_day_ago.isoformat():
            time_code = 2

        elif createdAt > one_week_ago.isoformat():
            time_code = 1

        else: 
            time_code = 0
        
        # location information
        country = user.get('country', None)
        state = user.get('state', None)
        city = user.get('city', None)

        lat = user.get('latitude', None)
        if lat is not None:
            print "lat (before): %f" % lat
            lat = round(lat, 2)
            print "lat (after): %f" % lat

        lng = user.get('longitude', None)
        if lng is not None:
            print "lat (before): %f" % lng
            lng = round(lng, 2)
            print "lat (after): %f" % lng

        # set location_str
        location_str = ""

        if country is None:
            location_str = ""

        # country not None
        elif city is None:
            location_str = country
        
        # country and city not None
        elif state is None:
            location_str = "%s, %s" % (city, country)

        # country, cit, state not None
        else:
            location_str = "%s, %s" % (city, state)

        # add to list
        location_list.append([location_str, lat, lng, time_code])

    # city_list = users.distinct("city")

    return json.dumps({"locations": location_list})


if __name__ == '__main__':
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("--host", dest="host", default="localhost",
    #                   help="hostname or ip address", metavar="host")
    # parser.add_option("--port", dest="port", default=8080,
    #                   help="port number", metavar="port")
    # run(app, host=options.host, port=int(options.port))

    run(app, host='172.31.16.215', port=80)

