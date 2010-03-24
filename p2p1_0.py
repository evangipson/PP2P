# asynchronous chat program
# programmers: evan gipson, nick hawkes
# peer-to-peer_1.0
# date: 3/20/2010
import wx
import os
import sys
from socket import *
import select
import thread

# get dest ip and dest port number
serverHost = raw_input("What IP address will you be visiting? ")
serverPort = input("Which port? ")
# set host ip and host port
myHost = ''
myPort = serverPort
# create a TCP socket
s = socket(AF_INET, SOCK_STREAM)
# function definition for client recieving data
def recv_data():
       while 1:
           try:
               recv_data = s.recv(1024)
           except:
               print "Server closed connection, thread exiting."
               thread.interrupt_main()
               break
               if not recv_data:
                   print "Server closed connection, thread exiting."
                   thread.interrupt_main()
                   break
           else:
               if recv_data == "q":
                   print "Server disconnected."
                   thread.interrupt_main()
                   break
               else:
                   print serverHost, ": ", recv_data
# function definition for server recieving data
def serv_recv_data():
       f = open("/home/nick/test.filename","wb")
       while 1:
              data = connection.recv(1024)
              if not data:
                     break
              f.write(data)
       f.close()
# function definition for client send data
def send_data():
       FILE = open("/p2p/03 Aint No Rest For The Wicked.mp3","rb")
       data = FILE.read()
       FILE.close()
       
       s.send(data)
# function definition for server send data
def serv_send_data():
   while 1:
       send_data = str(raw_input("Enter data to send (q to quit): "))
       if send_data == "q":
           s.send(send_data)
           thread.interrupt_main()
           break
       else:
           connection.send(send_data)
# if you aren't the first client, connect
try:
    s.connect((serverHost, serverPort))
except:
# if you are the first, you need to listen.
    print("I'm the first client, i'll listen.")
    s.bind((myHost, myPort))
    s.listen(5)
    connection, address = s.accept()
    connection_list.append(connection)
    print "Client (%s, %s) connected." % address
    thread.start_new_thread(serv_recv_data, ())
    thread.start_new_thread(serv_send_data, ())
    try:
        while 1:
               continue
    except:
        print "Server program quits.."         
        connection.close()

else:
# what to do if you connect successfully
    print("I'm not the first, i'll connect.")
    print "Connected to (%s, %s)." % (serverHost, serverPort) 
    thread.start_new_thread(recv_data,())
    thread.start_new_thread(send_data,())
    try:
        while 1:
            continue
    except:
        print "Client program quits.."
        s.close()
