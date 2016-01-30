import json
import httplib, urllib
import dateutil.parser
import pymongo
from operator import itemgetter
import os
import datetime, pytz
import json

import locale
locale.setlocale(locale.LC_ALL, ('en_US', 'utf-8'))

import sys
sys.path.insert(0, './Data Requests')
sys.path.insert(0, './Phone Number Lookup')

from get_class_data import returnClassData
from analyze_session import returnInsights
from phone_lookup_whitepages import returnDataForNumber

def get_pacific_time(time_str):

    time_datetime = dateutil.parser.parse(time_str)
    time_localized = pytz.utc.localize(time_datetime)
    return time_localized.astimezone(pytz.timezone('US/Pacific'))

# open/read config file
old_time = ""

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "last_updated.txt")

if os.path.isfile(file_path):
    with open (file_path, "r") as config_file:
        old_time = config_file.read().replace('\n', '')
        print "Old -- Pacific: %s  UTC: %s" % (get_pacific_time(old_time), old_time)

# record/print new last_updated time
new_time = datetime.datetime.utcnow().isoformat()
print "New -- Pacific: %s  UTC: %s" % (get_pacific_time(new_time), new_time)

# get data from Parse
user_data = returnClassData("_User", sort_by="createdAt", last_updated=old_time, new_updated=new_time)
link_data = returnClassData("Link", last_updated=old_time, new_updated=new_time)
logs_data = returnClassData("Logs", last_updated=old_time, new_updated=new_time)

# exit if no data returned
if user_data is None or link_data is None or logs_data is None:
    sys.exit("Error getting Parse data from module")

# print "New user data: %s \n" % user_data
# print "New link data: %s \n" % link_data
# print "New logs data: %s \n" % logs_data

# initialization
user_stats_list = []
print "Number of new/updated users: %u" % len(user_data)

# initialize mongo connection
connection = pymongo.MongoClient('localhost', 27017)
db = connection.test

# create users collection
users = db.users

# create user_stats_list
for user in user_data:
       
    user_objectId = user.get('objectId', None)
    
    # name else username
    user_name = user.get('name', None)

    if user_name is None: 
        user_name = user.get('username', None)

    user_username = user.get('username', None)
    user_createdAt = user.get('createdAt', None)
    user_mobile_number = user.get('mobile_number', None)

    user_stats = {
        "objectId": user_objectId,
        "createdAt": user_createdAt,
        "username": user_username,
        "mobile_number": user_mobile_number,
        "links_sent": 0,
        "friends": 0,
        "sessions": 0,
        "notifications": None,
        "device_model": None,
        "whitepages_data": None,
        "city": None,
        "state": None,
        "country": None,
        "latitude": None,
        "longitude": None,
        "verified": (user.get('mobile_number', None) is not None)
    }
    
    # special case 1: v1.* users who signed up with Facebook
    if (user.get('mobileVerified', None) is None and user.get('facebook_id', None) is not None):
        user_stats["verified"] = None

    # special case 2: v1.* users who created account with LinkMeUp
    if (user.get('mobileVerified', None) is None and user.get('mobile_number', None) is not None):
        user_stats["verified"] = None

    # reverse phone number look up
    if user_stats["mobile_number"] is not None:
        
        file_path = os.path.join(script_dir, ("Whitepages Data/%s_phone_data" % user_username))

        # data for user already exists
        if os.path.isfile(file_path):
            
            with open(file_path, 'r') as infile:
                result = json.loads(infile.read())

        else: # look up phone number and save result to file

            print user_stats["mobile_number"]

            if user_stats["mobile_number"][:1] == "+":
                result = returnDataForNumber(user_stats["mobile_number"][1:])
            else:
                result = returnDataForNumber(user_stats["mobile_number"])

            with open(file_path, 'w') as outfile:
                json.dump(result, outfile)        

        # process result
        best_location = result["results"][0]["best_location"]

        if best_location is not None:

            city = best_location["city"]
            state = best_location["state_code"]
            country = best_location["country_code"]
            latitude = best_location["lat_long"]["latitude"]
            longitude = best_location["lat_long"]["longitude"]

            user_stats["city"] = city
            user_stats["state"] = state
            user_stats["country"] = country
            user_stats["latitude"] = latitude
            user_stats["longitude"] = longitude

            print "User: %s  Location: %s, %s, %s" % (user_username, city, state, country)

    # add to user_stats_list
    user_stats_list.append(user_stats)

# link data
for link in link_data:

    link_createdAt = link.get('createdAt', None)

    sender_pointer = link.get('sender', None)
    sender_id = None

    if sender_pointer is not None:
        sender_id = sender_pointer.get('objectId', None)

    # number of links sent
    if any(user_stats['objectId'] == sender_id for user_stats in user_stats_list):

        index = map(itemgetter('objectId'), user_stats_list).index(sender_id)
        
        # increment links_sent, if haven't counted this link before
        if (not old_time or link_createdAt >= old_time): 
            user_stats_list[index]["links_sent"] += 1
 
# log data
for log in logs_data:

    log_createdAt = log.get('createdAt', None)

    user_pointer = log.get('user', None)
    user_id = None

    if user_pointer is not None:
        user_id = user_pointer.get('objectId', None)

    # users_stats corresponding to this objectId
    results_list = filter(lambda user_stats: user_stats['objectId'] == user_id, user_stats_list)
    user_stats = results_list[0] if results_list else None
    
    if user_stats is not None:
    
        # increment sessions, if haven't counted this session before
        if (not old_time or log_createdAt >= old_time):
            user_stats["sessions"] += 1

        # log insights
        insights = returnInsights(log)
        
        # print insights
        if user_stats["notifications"] is None:
            user_stats["notifications"] = insights["notifications"]

        if user_stats["device_model"] is None:
            user_stats["device_model"] = insights["device_model"]

# sort user_stats_list    
# user_stats_list_links = sorted(user_stats_list, key=itemgetter('links_sent'), reverse=True)
# user_stats_list_sessions = sorted(user_stats_list, key=itemgetter('sessions'), reverse=True)

# write new_time to config file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "last_updated.txt")

with open (file_path, "w") as config_file:
    config_file.write(new_time)
    config_file.truncate()

# insert into/update mongo database
for user_stats in user_stats_list:

    user_id = user_stats.get('objectId', None)
    user_username = user_stats.get('username', None)
    user_createdAt = user_stats.get('createdAt', None)

    user_links_sent = user_stats.get('links_sent', None)
    user_sessions = user_stats.get('sessions', None)
    user_verified = user_stats.get('verified', None)
    user_notifications = user_stats.get('notifications', None)
    user_device_model = user_stats.get('device_model', None)
    
    user_city = user_stats.get('city', None)
    user_state = user_stats.get('state', None)
    user_country = user_stats.get('country', None)
    user_latitude = user_stats.get('latitude', None)
    user_longitude = user_stats.get('longitude', None)

    user = db.users.find_one({"_id": user_id})
    
    # update, if already exists in DB
    if user is not None:
        db.users.update_one({"_id": user_id},
                            {"$set": {"verified": user_verified,
                                          "city": user_city,
                                         "state": user_state,
                                       "country": user_country,
                                      "latitude": user_latitude,
                                     "longitude": user_longitude,
                                    "links_sent": user["links_sent"] + user_links_sent,
                                      "sessions": user["sessions"] + user_sessions,
                                 "notifications": (user_notifications if user_notifications is not None else user["notifications"]),
                                  "device_model": (user_device_model if user_device_model is not None else user["device_model"])
        }})

    # insert into DB
    else:
        db.users.insert_one({"_id": user_id,
                             "username": user_username,
                             "createdAt": user_createdAt,
                             "verified": user_verified,
                             "city": user_city,
                             "state": user_state,
                             "country": user_country,
                             "latitude": user_latitude,
                             "longitude": user_longitude,
                             "links_sent": user_links_sent,
                             "sessions": user_sessions,
                             "notifications": user_notifications,
                             "device_model": user_device_model})

# print list
for user_stats in user_stats_list:

    user_id = user_stats.get('objectId', None)
    user_username = user_stats.get('username', None)
    user_createdAt = user_stats.get('createdAt', None)

    user_links_sent = user_stats.get('links_sent', None)
    user_sessions = user_stats.get('sessions', None)
    user_verified = user_stats.get('verified', None)
    user_notifications = user_stats.get('notifications', None)
    user_device_model = user_stats.get('device_model', None)

    user_city = user_stats.get('city', None)
    user_state = user_stats.get('state', None)
    user_country = user_stats.get('country', None)
    user_latitude = user_stats.get('latitude', None)
    user_longitude = user_stats.get('longitude', None)

    user_location_str = "%s, %s, %s" % (user_city[:12] if user_city is not None else user_city, user_state, user_country)

    print "%-20s  %-12s  Links sent: %-4u  Sessions: %-4u  Verified: %-7s  Notifs: %-7s  Device: %-11s  Location: %-22s" % (user_username[:18], user_id, user_links_sent, user_sessions, user_verified, user_notifications, user_device_model, user_location_str)
