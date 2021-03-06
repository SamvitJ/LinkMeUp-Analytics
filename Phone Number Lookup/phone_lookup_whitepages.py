import urllib, urllib2, json, os

def returnDataForNumber (mobile_number):
 
    # API key
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../Keys/keys.json")

    if os.path.isfile(file_path):
        with open(file_path, "r") as keys_file:
            keys = json.load(keys_file)

    else:
        print "Cannot find API key"
        return None

    url = "https://proapi.whitepages.com/3.0/phone.json"
    params = {
        'api_key': keys["whitepages"]["api-key"], 
        'phone': mobile_number
    }
    
    # print urllib.urlencode(params)
    # req = urllib2.Request(url, urllib.urlencode(params))
    
    req = urllib2.Request(url + '?api_key=' + params['api_key'] + '&phone=' + params['phone'])
    
    response = urllib2.urlopen(req)
    result = json.loads(response.read())

    return result
