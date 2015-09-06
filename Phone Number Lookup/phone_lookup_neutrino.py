import urllib, urllib2, json, os

def returnDataForNumber (mobile_number):

    # API key
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../Keys/keys.json")

    if os.path.isfile(file_path):
        with open(file_path, "r") as keys_file:
            keys = json.load(keys_file)

    else:
        print "Cannot find API keys"
        return None

    url = 'https://neutrinoapi.com/phone-validate'
    params = {
        'user-id': keys["neutrino"]["user-id"],
        'api-key': keys["neutrino"]["api-key"],
        'number': mobile_number
    }

    req = urllib2.Request(url, urllib.urlencode(params))
    
    response = urllib2.urlopen(req)
    result = json.loads(response.read())

    return result

