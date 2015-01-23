# supervisor-pagerduty
Python script to trigger pagerduty API on supervisord events with fatal status

# Usage
Script is triggered on supervisord events. On fatal process states it will create an incident on pagerduty and resolve this incident automatically after program is in running state again.

# Pagerduty configuration
Mostly supervisord will restart the program successfully. So it may be useful to configure the users notification rules to send mails, sms, push notifications etc. not immediately but after a minute. So you won't get bothered until supervisord handlet the problem by itself.

# Installation
Copy the pagerduty.py into e.g. /etc/supervisor folder and make it executable
    cd /etc/supervisor
    wget https://github.com/tak-aryelle/supervisor-pagerduty/raw/master/pagerduty.py
    chmod 755 pagerduty.py
    
Add pagerduty.conf to your supervisord config file, adjust path and add your API key, then update supervisor:
    supervisorctl reread
    supervisorctl update
    supervisorctl add pagerduty
    
Done.
