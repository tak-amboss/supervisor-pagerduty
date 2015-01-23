# supervisor-pagerduty
Python script to trigger pagerduty API on supervisord events with fatal status

# Usage
Script is triggered on supervisord events. On fatal process states it will create an incident on pagerduty and resolve this incident automatically after program is in running state again.

# Pagerduty configuration
Mostly supervisord will restart the program successfully. So it may be useful to configure the users notification rules to send mails, sms, push notifications etc. not immediately but after a minute. So you won't get bothered until supervisord handlet the problem by itself.
