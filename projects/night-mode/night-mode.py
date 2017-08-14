#!/usr/bin/env python3

import subprocess
import argparse
import time
import sys

def main():


	parser = argparse.ArgumentParser(description="Get the system prepared for sleep")
	parser.add_argument('-b', '--backlight', type=int, metavar='<b>', help="Backlight value (default 1), set to -1 to ignore", default=1)
	parser.add_argument('-t', '--timer', type=str, metavar='<t>', help='Time to close the system', default=0)
	parser.add_argument('-c', '--close', type=str, metavar='<c>', help="Action to take when timer is done", default="suspend")

	args = parser.parse_args()
	print(args)

	closecmd = None
	closeaction = args.close
	if(closeaction in ['suspend', 'sleep']):
		closecmd = 'systemctl suspend'
	elif(closeaction in ['poweroff', 'shutdown']):
		closecmd = 'systemctl poweroff'
	elif(closeaction in ['displayoff', 'display', 'screenoff', 'screen']):
		closecmd = 'xset dpms force off'
	elif(closeaction == 'hibernate'):
		closecmd = 'systemctl hibernate'
	else:
		print("Unknown close command: " + closeaction)
		return

	set_backlight(args.backlight)
	start_close_timer(args.timer)
	subprocess.Popen(closecmd.split())

def set_backlight(amount):
	if amount < 0:
		pass
	elif amount == 0:
		subprocess.Popen(['xset', 'dpms', 'force', 'off'])
	else:
		subprocess.Popen(["xbacklight", "-set", str(amount)])

def start_close_timer(rawtime):
	unitkey = rawtime[len(rawtime)-1]
	timeval = rawtime[0:len(rawtime)-1]
	if(unitkey == 's'):
		time.sleep(float(timeval))
	elif(unitkey == 'm'):
		time.sleep(float(timeval) * 60)
	elif(unitkey == 'm'):
		time.sleep(float(timeval) * 60 * 60)
	else:
		time.sleep(float(rawtime))

if __name__ == "__main__":
	main()
