#!/usr/bin/python3
# Automatic txpower increase and/or starting monitor mode
# Author:demontager


from os import getuid, devnull
from re import findall
from sys import argv, stdout, stdin
from time import sleep
from subprocess import call, check_output


# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
  
args = argv[1:]
POWER = '30dbm'
DN = open(devnull, 'w')
DUMP = '/tmp/dump.cap'

def msg():
	print(O+"Automatic txpower increase on RTL8187 chip aka \"Alfa Awus036\"\n"+'and/or starting monitor mode'+W+"\n")
	print(G+'txpower usage:' +GR+'<power/start/stop/all> <interface> <channel>'+W+"\n")
	print(G+'Options:'+W)
	print('power    :set ', POWER)
	print('start    :enable monitor mode and airodump-ng')
	print('stop     :disable monitor mode')
	print('all      :set' , POWER, 'enable monitor mode and airodump-ng')
	print('channel  :set desired channel 1-13 (optional)')
	print("")

if len(args) == 2:
    pass
elif len(args) == 3:
	CH = args[2]	
else:
    msg()
    exit(1)

IFACE = args[1]

def monif():
	MONIF = findall('mon[0-9]', str(check_output(['iwconfig'],stderr=DN)))
	if MONIF != []:
	    return MONIF[0]
	else:
		return ''   
	
def check_iface():
    iface = call(['iwconfig', IFACE], stdout=DN, stderr=None)
    if iface != 0:
        msg()	
        exit(1)
		 	
def power(): 
    check_iface()
    xd = str(check_output(['iwconfig', IFACE]))
    if 'Not-Associated' in xd:	
        call(['ifconfig', IFACE, 'down'])
        call(['iw', 'reg', 'set', 'BO'])
        call(['iwconfig', IFACE, 'txpower', POWER])
        call(['ifconfig', IFACE, 'up'])
        z = findall('Tx-Power=[1-9][0-9]', xd) 
        print(z[0],'dBm')
    else:
        print (GR+'Disconnect from WiFi-AP first'+W)

def start():
	check_iface()
	if not findall('mon[0-9]', monif()) and len(args) == 2:
		call(['airmon-ng', 'start', IFACE])
		sleep(3)
		call(['airodump-ng', '-w', DUMP, '--ignore-negative-one', monif()])
	if not findall('mon[0-9]', monif()) and len(args) == 3:
	    call(['airmon-ng', 'start', IFACE])
	    sleep(3)
	    call(['airodump-ng', '-w', DUMP, '-c', CH, '--ignore-negative-one', monif()])
	else:
		print(G+'Already has monitor mode on:', monif()+W)	

def stop():
	if monif() == '':	
	    print(G+'Monitor mode already stopped'+W)
	else:
			call(['airmon-ng', 'stop', IFACE])
    
x = getuid()
if x != 0:
	print(G+'You have to be'+R+' root ' +G+'to run this script'+W)
	exit(1)

try:
	if argv[1] == 'power':
		power()
	elif argv[1] == 'start':
		start()	
	elif argv[1] == 'stop':
		stop()
	elif argv[1] == 'all':
		power()
		sleep(3)
		start()
except KeyboardInterrupt:
	print(G+'Operation aborted, shutting down monitor mode...'+W)
	call(['airmon-ng', 'stop', monif()])
	print('\r\n')
	exit()
				
