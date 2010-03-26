# peer to peer program
# programmers: evan gipson, nick hawkes
# peer-to-peer_1.0
# date: 3/20/2010
import wx
import os
import sys
from socket import *
import select
import thread
import urllib
#determine how big a chunk is
def chunk(file_size):
       file_size = file_size/4.0
       return file_size
#determine where to start seeking
def part(file_size, part):
       part = file_size * part
       return part
#create/open a file in 'wb', re-assemble data
def recv_data(part, size_of_file, filename):
       #get filename path
       path = '/p2p/files/' + filename
       #open file to write binary
       FILE = open(path,'wb')
       FILE.seek(part)
       chunk = chunk(size_of_file)
       while 1:
           recv_data = s.recv(chunk)
           if not data:
              FILE.close()
              print 'File complete!'
              break
           else:
              FILE.write(chunk)
       FILE.close()
#open the file in 'rb', chunk up data
def send_data(size_of_file, filename):
       #get filename path
       path = '/p2p/files/' + filename
       #open file to send
       FILE = open(path,'rb')
       data = FILE.read()
       #get values to read
       chunk = chunk(size_of_file)
       part = part(chunk, part)
       try:
           FILE.seek(part)
       except:
           print 'File corrupt/not correct size'
           FILE.close()
       else:
          #read your data
          data = FILE.read(chunk)
          #close the file
          FILE.close()
          #send your chunk
          s.send(data)
#main loop
def work(i,size_of_file, filename):
       #specify host ip and port num
       serverHost = ip[i]
       serverPort = 9000
       #specify part your getting from host
       newpart = part[i]
       #specify your ip and port num
       myHost = ''
       myPort = 9000
       #create a TCP socket for clients
       s = socket(AF_INET, SOCK_STREAM)
       print 'Before the try block'
       #connect to server
       try:
              s.connect((serverHost, serverPort))
       #if you can't connect, try to listen
       except:
              print 'client not ready'
              s.bind((myHost, myPort+1))
              s.listen(5)
              s, address = s.accept()
              try:
                  while 1:
                     continue
              except:
                     print "program quits.."         
                     connection.close()
                     s.close()
       else:
              recv_data(newpart, size_of_file, filename)
              try:
                  while 1:
                     continue
              except:
                  print 'program quits...'
                  s.close()
#see website for available files
#   -have link for file download
#   -http://cs5550.webs.com/aint_no_rest.tracer
filename = raw_input("What file would you like to download? ")
path = 'http://cs5550.webs.com/' + filename + '.tracker'
try:
       f = urllib.urlopen(path)
except:
       print 'Invalid filename specified.'
else:
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
       #size of file is the last entry, minus newline
       size_of_file = newlist.pop()
       #break it down - ip's and parts
       for i in range(len(newlist)):
           ip.append(newlist[i][0])
           part.append(newlist[i][1])
       print ip
       print part
       #giant for loop
       time = len(ip)    
       for i in range(time - 1):
              #thread the work process
              #for efficiency
              work(i, size_of_file[0], filename)
