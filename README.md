LinkMeUp-Analytics is an analytics suite to process user data from LinkMeUp, and the backend to www.linkmeupmessenger.com/map. 

**How it works**

[run\_analytics.sh](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/run_analytics.sh) ([calc\_user\_stats.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/calc_user_stats.py)) runs as a cron job on an AWS EC2 ubuntu instance, periodically updating a local MongoDB collection with data pulled from LinkMeUp's backend database via [get\_class\_data.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Data%20Requests/get_class_data.py).

In particular, [calc\_user\_stats.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/calc_user_stats.py) uses module [phone\_lookup\_whitepages.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Phone%20Number%20Lookup/phone_lookup_whitepages.py) to get location data for new users, and module [analyze\_session.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/analyze_session.py) to extract insights from session logs.

Finally, [backend.py](https://github.com/SamvitJ/LinkMeUp-Analytics/blob/master/Web%20Backend/backend.py) using the microframework Bottle to run the web server for www.linkmeupmessenger.com/map. In response to AJAX requests from the map, it queries the mongo collection for valid records and returns an aggregated list of cities (including coordinates and time codes) with LinkMeUp users.
