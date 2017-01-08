LinkMeUp-Analytics is the backend to a dynamic, Google Maps-based visualization of the LinkMeUp userbase (http://www.linkmeupmessenger.com/map/).

**How it works**

[calc\_user\_stats.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/calc_user_stats.py) runs as a [cron job](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/crontab) on an AWS EC2 instance, periodically updating a local MongoDB collection with data pulled from LinkMeUp's backend database via [get\_class\_data.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Data%20Requests/get_class_data.py).

In particular, [calc\_user\_stats.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/calc_user_stats.py) uses module [phone\_lookup\_whitepages.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Phone%20Number%20Lookup/phone_lookup_whitepages.py) to get location data for new users, and module [analyze\_session.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/analyze_session.py) to extract insights from session logs.

Finally, [backend.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Web%20Backend/backend.py) acts as the web server backend to the userbase map. In response to AJAX requests from the frontend, it queries the mongo collection for valid records and returns data on cities with LinkMeUp users.
