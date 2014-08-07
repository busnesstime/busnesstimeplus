# -*- coding: utf-8 -*-
import json
import requests
import arrow # better datetime lib http://crsmithdev.com/arrow/
import pprint
import math

url = 'http://nxtbus.act.gov.au/departures'
date_now = arrow.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
payload = {"stopId":"6350786798486033481","stopType":"BUS_STOP","departureDate":date_now,"departureTime":date_now,"departureOrArrival":"DEPARTURE"}
headers = {'User-Agent': "Busness Time+ <maxious@lambdacomplex.org>", 'Content-Type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain, */*'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
data = r.json()
print u"\U0001F68F  Stop Number "+ payload['stopId']
print  ''
for service in data['body']:
	service['realTimeDeparture'] = service['realTimeDeparture']/1000
	service['realTimeDepartureTime'] = arrow.get(service['realTimeDeparture']).to('Australia/Canberra')
	service['realTimeDepartureMinute'] = arrow.get(service['realTimeDeparture']).to('Australia/Canberra').format('m')
	service['scheduledDeparture'] = service['scheduledDeparture']/1000
	service['scheduledDepartureTime'] = arrow.get(service['scheduledDeparture']).to('Australia/Canberra')
	service['delay'] = service['realTimeDeparture']-service['scheduledDeparture']
	#pprint.pprint(service)
	print u'\U0001F68C ' + '  ' + service['serviceNumber'] + u' \u27A1 ' + service['destination'] 
	for stopAsset in service['stopAssets']:
		if stopAsset['value'] == 'true':
			if stopAsset['type'] == "HAS_LOW_FLOOR":
				print u"\u267F"
			if stopAsset['type'] == "HAS_BIKE_RACK":
				print u"\U0001F6B4"
	if service['realTimeDeparture'] == service['scheduledDeparture']:
		print eval('u"\U0001F5%x"' % (80 + int(math.ceil(float(service['realTimeDepartureMinute'])/60*12)))) + '  ' + service['realTimeDepartureTime'].format('HH:mm:ss')
	else:
		print eval('u"\U0001F5%x"' % (80 + int(math.ceil(float(service['realTimeDepartureMinute'])/60*12)))) + '  ' + service['realTimeDepartureTime'].humanize()
	if service['delay'] > 60:
		print u"\U0001F494  " + str(int(math.ceil(service['delay']/60))) + " minute delay"
	print ''
