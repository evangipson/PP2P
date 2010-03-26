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
#global variables
global size_of_chunk
#determine how big a chunk is
def chunk(file_size):
       final_file_size = file_size/4
       return final_file_size
#determine where to start seeking
def part(file_size, secure_part):
       final_part = file_size * (secure_part - 1)
       return final_part      
#main loop
def work(i,ip,size_of_file, filename, secure_part):
       #specify host ip and port num
       serverHost = ip[i]
       serverPort = 9010
       #specify part your getting from host
       newpart = secure_part
       #specify your ip and port num
       myHost = ''
       myPort = 9010
       #create a TCP socket for clients
       new_socket = socket(AF_INET, SOCK_STREAM)
       #connect to server
       try:
              new_socket.connect((serverHost, serverPort))
       #if you can't connect, try to listen
       except:
            print 'client not ready'
            new_socket.bind((myHost, myPort))
            new_socket.listen(5)
            connection, address = new_socket.accept()
            print 'client connected'
            #get filename path
            path = '/p2p/files/' + filename
            #open file to send
            FILE = open(path,'rb')
            print 'opened file for sending...'
            data = FILE.read()
            #get values to read
            newpart = part(size_of_chunk, secure_part)
            try:
                FILE.seek(newpart)
            except:
                print 'File corrupt/not correct size'
                FILE.close()
            else:
                #read your data
                sending_data = FILE.read(size_of_chunk)
                #close the file
                FILE.close()
                #send your chunk
                print 'sending data...'
                connection.send(sending_data)
                connection.close()
       else:
            print 'connected to host' #get filename path
            path = '/p2p/files/' + filename
            #open file to write binary
            FILE = open(path,'wb')
            newpart = part(size_of_chunk, secure_part)
            FILE.seek(newpart)
            print filename + ' downloading...'
            while 1:
                recv_data = new_socket.recv(size_of_chunk)
                if not data:
                   FILE.close()
                   print 'File complete!'
                   break
                else:
                   FILE.write(recv_data)
                   FILE.close()  
                s.close()
#see website for available files
#   -have link for file download
#   -http://cs5550.webs.com/aint_no_rest.tracker
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
       temppart = []
       securepart = []
       #get the list of IP's 
       newlist = [i.split(',') for i in s]
       #get the last entry out of there
       newlist.pop()
       #size of file is the last entry, minus newline
       size_of_file = newlist.pop()
       size_of_chunk = chunk(int(size_of_file[0]))
       #break it down - ip's and parts
       for i in range(len(newlist)):
           ip.append(newlist[i][0])
           temppart.append(newlist[i][1])
       for num in temppart:
           securepart.append(int(num))
       #giant for loop
       time = len(ip)    
       for i in range(time - 1):
              #thread the work process
              #for efficiency
              work(i,ip, size_of_file, filename, securepart[i])
