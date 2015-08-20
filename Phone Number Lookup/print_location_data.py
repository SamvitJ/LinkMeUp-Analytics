import os
import sys
import json


def main(argv):

    if len(argv) > 1:
        username = argv[1]

    else:
        print "Usage %s - must specify username" % argv[0]
        return

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../Whitepages Data/%s_phone_data" % username)

    if os.path.isfile(file_path):

        with open(file_path, "r") as result_file:

            json_result = json.loads(result_file.read())
            location = json_result["results"][0]["best_location"]

            print json.dumps(location, sort_keys=True, indent=4)

    else:
        print "Couldn't find file"

# execute main
if __name__ == "__main__":
    main(sys.argv)
