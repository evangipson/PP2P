import os
import sys
from socket import *
import select
import thread
import urllib
#see website for available files
#   -have link for file download
#   -http://cs5550.webs.com/aint_no_rest.tracker
f = urllib.urlopen("http://cs5550.webs.com/aint_no_rest.tracker")
s = f.read()
f.close()

print s
#read the file
#   -in /p2p/tracker

#get the list of IP's
#create a socket
#connect to the IP's
#populate the file list

