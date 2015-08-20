import os
import datetime, dateutil.parser, pytz

# open/read config file
old_time = ""

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "last_updated.txt")

if os.path.isfile(file_path):
    with open (file_path, "r") as config_file:
        old_time = config_file.read().replace('\n', '')
        old_time_datetime = pytz.utc.localize(dateutil.parser.parse(old_time))
        print "Pacific: %s  UTC: %s" % (old_time_datetime.astimezone(pytz.timezone('US/Pacific')), old_time)
