
import pymongo
import json
import datetime
import time
import pytz
from bottle import Bottle, request, response, run
import cherrypy

app = Bottle()

# this is the handler for the default path of the web server

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/', method=['OPTIONS', 'GET'])
def index():

    # start time
    # start_time = time.time()

    # connect to mongoDB
    connection = pymongo.MongoClient('localhost', 27017)

    # attach to test database
    db = connection.test

    # get handle for users collection
    users = db.users

    # mongo init time
    # mongo_init_time = time.time()

    # return all users with valid location coordinates
    all_users = users.find( { "$and": [{"latitude" : {"$ne": None}}, {"longitude": {"$ne": None}}] })

    # mongo query time
    # mongo_query_time = time.time()

    # reference time (used for time code)
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    # print "%s %s" % (one_day_ago, one_week_ago)

    # create array of locations
    location_list = []

    for user in all_users:

        # location str
        location_str = ""

        country = user.get('country', None)
        state = user.get('state', None)
        city = user.get('city', None)

        if country is None:
            location_str = ""

        # country not None
        elif city is None:
            location_str = country
        
        # country and city not None
        elif state is None:
            location_str = "%s, %s" % (city, country)

        # country, city, state not None
        else:
            location_str = "%s, %s" % (city, state)

        # latitude/longitude
        lat = user.get('latitude', None)
        if lat is not None:
            lat = round(lat, 2)

        lng = user.get('longitude', None)
        if lng is not None:
            lng = round(lng, 2)

        # determine time code
        createdAt = user.get('createdAt', None)
        time_code = 3

        if createdAt >= one_hour_ago.isoformat():
            time_code = 0

        elif createdAt >= one_day_ago.isoformat():
            time_code = 1

        elif createdAt >= one_week_ago.isoformat():
            time_code = 2

        else:
            time_code = 3

        # if location string/time code pair already contained, skip
        if any(loc[0] == location_str and loc[3] == time_code for loc in location_list):
            # print "%s %s %u" % (user.get('username', None), location_str, time_code)
            continue
        
        # otherwise, add to list
        location_list.append([location_str, lat, lng, time_code])

    # city_list = users.distinct("city")

    # data generation time
    # data_gen_time = time.time()

    # print time taken
    # print "%f %f %f" % (mongo_init_time - start_time,
    #                     mongo_query_time - mongo_init_time,
    #                     data_gen_time - mongo_query_time)

    # print time of request
    pacific = pytz.timezone("US/Pacific")
    print datetime.datetime.now(pacific)

    return json.dumps({"locations": location_list})


if __name__ == '__main__':
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("--host", dest="host", default="localhost",
    #                   help="hostname or ip address", metavar="host")
    # parser.add_option("--port", dest="port", default=8080,
    #                   help="port number", metavar="port")
    # run(app, host=options.host, port=int(options.port))

    run(app, host='172.31.16.215', port=80, server='cherrypy')

