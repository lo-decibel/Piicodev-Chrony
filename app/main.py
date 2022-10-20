#!/usr/bin/python3
import ntplib
from os import system, getenv
from datetime import datetime, timedelta
from PiicoDev_RV3028 import PiicoDev_RV3028
from pythonping import ping
from time import sleep

def online():
	try:
		for response in ping(getenv('NTP_SERVER')):
			if response.success:
				return True
	except:
		return False

def ntp_time(server):
	return datetime.utcfromtimestamp(int(ntp_client.request(server, version=3).tx_time))

def piicodev_time():
	p.getDateTime()
	return datetime(p.year + 2000, p.month, p.day, p.hour, p.minute, p.second)

def chrony_set(t):
	system('chronyc manual on')
	new_time = t.strftime('%b %d, %Y %H:%M:%S')
	system('chronyc settime ' + new_time) != 0

def piicodev_set(t):
	p.year = t.year
	p.month = t.month
	p.day = t.day
	p.hour = t.hour
	p.second = t.second
	p.weekday = t.weekday()
	p.setDateTime()

p = PiicoDev_RV3028()
ntp_client = ntplib.NTPClient()

while True:
	sleep(30)
	
	if online():
		try:
			while abs(ntp_time('127.0.0.1') - ntp_time(getenv('NTP_SERVER'))) > timedelta(seconds=1):
				sleep(1)
			piicodev_set(ntp_time('127.0.0.1'))
			print('Set Piicodev RTC clock to Chrony time.')
			break
		except:
			print('Error setting time on Piicodev clock.')
			continue
	
	else:
		try:
			if ntp_time('127.0.0.1') - piicodev_time() < timedelta(seconds=1):
				chrony_set(piicodev_time())
				print('Set Chrony time to Piicodev RTC clock.')
				break
			
		except:
			print('Error setting time on Chrony.')
			continue
		
		while True:
			try:
				if online():
					system('chronyc manual off')
					system('chronyc -a burst 4/4')
					piicodev_set(ntp_time('127.0.0.1'))
			except:
				sleep(1)
				continue

print('Clocks synced')