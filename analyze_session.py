import sys

def returnInsights (session_logs):

   insights = {
      "notifications" : None,
      "device_model": None
   }

   notifications_none = "Notifications - None"
   notifications_alert = "Notifications - Alert"
   notifications_badge = "Notifications - Badge"
   notifications_sound = "Notifications - Sound"
   notifications_content = "Notifications - ContentAvailability"

   device_model_4 = "iPhone 4"
   device_model_5 = "iPhone >= 5"

   for log in session_logs["messages"]:

      # notifications
      if notifications_none in log:
         insights["notifications"] = "Off"

      elif notifications_alert in log:
         insights["notifications"] = "Alert"

      elif any(str in log for str in [notifications_badge, notifications_sound, notifications_content]):
         insights["notifications"] = "Other"

      # device
      if device_model_4 in log:
         insights["device_model"] = "iPhone 4"

      elif device_model_5 in log:
         insights["device_model"] = "iPhone 5+"

   return insights 
 
