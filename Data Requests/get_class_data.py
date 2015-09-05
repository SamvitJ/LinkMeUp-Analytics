import json
import httplib, urllib
import os
import datetime

def returnClassData (parse_class_name, sort_by="updatedAt", last_updated="", new_updated=""):

    # paging
    skip = 0
    limit = 1000

    all_data = []

    while True:

        connection = httplib.HTTPSConnection('api.parse.com', 443)

        # create parameter dictionary
        params_dict = {
            "limit": limit,
            "skip": skip,
            "order": sort_by
        }
        # add updatedAt constraint, if parameters provided
        if last_updated and new_updated:
            params_dict["where"] = json.dumps({
                "updatedAt": {
                    "$gte": {
                        "__type": "Date",
                        "iso": last_updated
                    },
                    "$lt": {
                        "__type": "Date",
                        "iso": new_updated
                    }
                }
            })
        params = urllib.urlencode(params_dict)

        # Parse keys
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "../Keys/keys.json")

        if os.path.isfile(file_path):
            with open(file_path, "r") as keys_file:
                keys = json.load(keys_file)

        connection.connect()
        connection.request('GET', '/1/classes/%s?%s' % (parse_class_name, params), '', {
               "X-Parse-Application-Id": keys["parse"]["app-id"],
               "X-Parse-REST-API-Key": keys["parse"]["api-key"]
             })
        result = json.loads(connection.getresponse().read())

        request_data = result.get('results', None)

        if not request_data:
            break

        all_data.extend(request_data)
        skip = skip + limit

    return all_data
