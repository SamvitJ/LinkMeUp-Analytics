LinkMeUp-Analytics is an analytics suite to process user data from LinkMeUp, and the backend to www.linkmeupmessenger.com/map. 

How it works:
run\_analytics.sh (calc\_user\_stats.py) runs as a scheduled cron job on an AWS EC2 instance and periodically updates a local mongo collection with data pulled from Parse, LinkMeUp's backend database (get\_class\_data.py).
In particular, calc\_user\_stats.py uses module phone\_lookup\_whitepages.py to get location data for new users, and stores this info, along with other insights extracted from session logs (analyze\_session.py), to the mongo collection.
Web Backed/backend.py - as its name implies - responds to AJAX requests from www.linkmeupmessenger.com/map, returning an aggregated list of cities/time codes with LinkMeUp users.
