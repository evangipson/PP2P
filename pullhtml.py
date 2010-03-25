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
#read the file
s = f.read().split('\n')
f.close()
#initializing lists
ip = []
part = []
#get the list of IP's
newlist = [i.split(',') for i in s]
#get the last entry out of there
newlist.pop()
for address in range(len(newlist)):
    ip.append(newlist[address][0])
    part.append(newlist[address][1])
print ip
print part
#create a socket
#connect to the IP's
#populate the file list

