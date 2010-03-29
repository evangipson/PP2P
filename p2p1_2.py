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
def chunk(file_size,how_many):
       final_file_size = file_size/how_many
       return final_file_size
#determine where to start seeking
def part(file_size, secure_part):
       final_part = file_size * (secure_part - 1)
       return final_part
def ListenWork(data, secure_part, filename, extension):
       myHost = ''
       myPort = 9008
       listen_socket = socket(AF_INET,SOCK_STREAM)
       listen_socket.bind((myHost, myPort+i))
       listen_socket.listen(5)
       connection, address = listen_socket.accept()
       print 'client connected'
       thread.interrupt_main()
       path = '/p2p/files/' + filename + extension
       #open file to send
       FILE = open(path,'rb')
       print 'opened', filename, 'for sending...'
       data = FILE.read()
       FILE.close()
        #get values to read
       newpart = part(size_of_chunk, secure_part)
       try:
              FILE.seek(newpart)
       except:
              print 'File corrupt/not correct size'
              FILE.close()
              connection.close()
              thread.interrupt_main()
       else:
              #read your data
              sending_data = FILE.read(size_of_chunk)
              #close the file
              FILE.close()
              #send your chunk
              print 'sending data...'
              connection.send(sending_data)
              connection.close()
              thread.interrupt_main()
#main loop
def work(i,ip,size_of_file, filename, extension, secure_part):
       #specify host ip and port num
       serverHost = ip[i]
       serverPort = 8060
       #create a TCP socket for clients
       new_socket = socket(AF_INET, SOCK_STREAM)
       #connect to server
       try:
            new_socket.connect((serverHost, serverPort+i))
       #if you can't connect, try to listen
       except:
            print 'clients not connected yet.'
       else:
            print 'connected to host' #get filename path
            path = '/p2p/files/' + filename + extension
            #open file to write binary
            FILE = open(path,'wb')
            newpart = part(size_of_chunk, secure_part)
            FILE.seek(newpart)
            print filename + ' downloading...'
            while 1:
                recv_data = new_socket.recv(size_of_chunk)
                if not recv_data:
                   FILE.close()
                   print 'File complete!'
                   new_socket.close()
                   break
                else:
                   FILE.write(recv_data)

#see website for available files
#   -have link for file download
n = urllib.urlopen('http://cs5550.webs.com/file_list')
#put into a list
file_list = n.read().split('\n')
#initialize lists for storage
temp_file_list = []
temp_ext_list = []
#break up extensions
new_file_list = [i.split(',') for i in file_list]
#get empty off the list
new_file_list.pop()
for i in range(len(new_file_list)):
       temp_file_list.append(new_file_list[i][0])
       temp_ext_list.append(new_file_list[i][1])
#show the list of files and index
#while loop
while 1:
       print 'List of files'
       print '-------------'
       for i in range(len(temp_file_list)):
              new_file_name = temp_file_list[i]+ temp_ext_list[i]
              print i+1, ':', new_file_name
       file_number = input("Number of file to download (0 to quit): ")
       #check if quit
       if file_number == 0:
              print 'Exiting...'
              break
       #specify filename using index
       filename = temp_file_list[file_number-1]
       extension = temp_ext_list[file_number-1]
       print filename, extension
       path = 'http://cs5550.webs.com/' + filename + '.tracker'
       f = urllib.urlopen(path)
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
       #contains size in bytes and how much to split
       size_of_file = newlist.pop()
       size_of_chunk = chunk(int(size_of_file[0]),int(size_of_file[1]))
       #break it down - ip's and parts
       for i in range(len(newlist)):
           ip.append(newlist[i][0])
           temppart.append(newlist[i][1])
       for num in temppart:
           securepart.append(int(num))
       #download loop
       do_you = raw_input('would you like to serve files? ')
       if do_you == 'y':
              for i in range(int(size_of_file[1])):
                     ListenWork(i, int(size_of_file[1]), filename, extension)
       else:
              for i in range(int(size_of_file[1])):  
                     work(i,ip, int(size_of_file[0]), filename, extension, securepart[i])
