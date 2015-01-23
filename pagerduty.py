#!/usr/bin/env python
#
# Script originally by Sam Hocevar <sam@hocevar.net> (2004)
# Refined by tak-aryelle <https://gist.github.com/tak-aryelle> (2015)
#

import urllib2
import json
from supervisor import childutils
import sys
import socket
import time

class PagerDutyNotifier(object):
    def __init__(self, pd_service_key):
        self.pd_service_key = pd_service_key
        self.pd_url = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'
        self.status = True
    def run(self):
        while True:
            headers, payload = childutils.listener.wait()
            sys.stderr.write(str(headers) + '\n')
            payload = dict(v.split(':') for v in payload.split(' '))
            sys.stderr.write(str(payload) + '\n')
            if headers['eventname'] == 'PROCESS_STATE_FATAL':
                details = {}
                self.send(payload, headers, 'trigger', '{} service has crashed unexpectedly on {}'.format(payload['processname'], socket.gethostname()), details)
            if headers['eventname'] == 'PROCESS_STATE_RUNNING':
                details = { 'fixed at': time.strftime("%c") }
                self.send(payload, headers, 'resolve', 'Process recreated by supervisor', details)
            if self.status:
                childutils.listener.ok()
            else:
                childutils.listener.fail()
                self.status = True
            sys.stderr.flush()
    def send(self, payload, headers, event_type, description, details):
        incident_key = '{}/{}'.format(socket.gethostname(), payload['processname'])
        client = '{}'.format(headers['server'])

        details = dict(details, **headers)
        details = dict(details, **payload)

        data = {'service_key':  self.pd_service_key,
                'incident_key': incident_key,
                'event_type':   event_type,
                'description':  description,
                'client':       client,
                'details':	     details
        }
        try:
            res = urllib2.urlopen(self.pd_url, json.dumps(data))
        except urllib2.HTTPError, ex:
            sys.stderr.write('{} - {}\n{}\n'.format(ex.code, ex.reason, ex.read()))
            self.status = False
        else:
            sys.stderr.write('{}, {}\n'.format(res.code, res.msg))

if __name__ == '__main__':
    pager_duty_service_key = sys.argv[1]
    pager_duty_notifer = PagerDutyNotifier(pager_duty_service_key)
    pager_duty_notifer.run()

