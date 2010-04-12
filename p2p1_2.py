# peer to peer program
# programmers: evan gipson, nick hawkes
# peer-to-peer_1.0
# date: 3/20/2010
import os
import sys
from socket import *
import thread
import urllib
from itertools import cycle

#progress bar class
class ProgressBar(object):
    """Visualize a status bar on the console."""

    def __init__(self, max_width):
        """Prepare the visualization."""
        self.max_width = max_width
        self.spin = cycle(r'-\|/').next
        self.tpl = '%-' + str(max_width) + 's ] %c %5.1f%%'
        show(' [ ')
        self.last_output_length = 0

    def update(self, percent):
        """Update the visualization."""
        # Remove last state.
        show('\b' * self.last_output_length)

        # Generate new state.
        width = int(percent / 100.0 * self.max_width)
        output = self.tpl % ('-' * width, self.spin(), percent)

        # Show the new state and store its length.
        show(output)
        self.last_output_length = len(output)
        
def show(string):
    """Show a string instantly on STDOUT."""
    sys.stdout.write(string)
    sys.stdout.flush()
def percentize(steps):
    """Generate percental values."""
    for i in range(steps + 1):
       yield i * 100.0 / steps
       
#create a tracker
def create(filename, extension):
       path = '/home/evan/' + filename + '.tracker'
       new_path = '/p2p/files/' + filename + extension
       file_size = os.path.getsize(new_path)
       #information list for returns
       information = []
       #chunk up file to 1000 bytes a piece
       new = file_size/512000
       #get remainder
       rem = file_size%512000
       #open file for writing the tracker to
       FILE = open(path,'w')
       #find my IP out
       s = socket(AF_INET, SOCK_STREAM)
       s.connect(('www.google.com',80))
       my_ip = s.getsockname()
       s.close()
       #start writing
       for i in range(new):
             FILE.write(str(my_ip[0])+','+str(i+1)+','+'512000\n')
       FILE.write(str(my_ip[0])+','+str(new+1)+','+str(rem)+'\n')
       FILE.write(str(file_size)+','+str(new+1))
       #close file up
       FILE.close()
       #return file size and how many pieces (0 doesn't count)
       return [file_size,(new+1),rem]

#determine where to start seeking
def part(file_size, secure_part):
       final_part = file_size * (secure_part)
       return final_part

def ListenWork(i,file_size, filename, extension, parts,rem):
       myHost = ''
       myPort = 9010 + i
       for i in range(parts):
              listen = socket(AF_INET,SOCK_STREAM)
              listen.bind((myHost, myPort))
              listen.listen(parts)
              connection, address = listen.accept()
              #print 'client connected'
              path = '/p2p/files/' + filename + extension
              #open file to send
              FILE = open(path,'rb')
              #print 'opened', filename, 'for sending...'
              data = FILE.read()
              newpart = part(file_size, i)
              try:
                     FILE.seek(newpart)
              except:
                     print 'File corrupt/not correct size'
                     FILE.close()
                     connection.close()
                     listen_socket.close()
                     thread.interrupt_main()
                     break
              else:
                     #read your data
                     if (i == parts):
                         sending_data = FILE.read(rem)
                     else:
                         sending_data = FILE.read(512000)
                     #close the file
                     FILE.close()
                     #send your chunk
                     #print 'sending data...'
                     connection.send(sending_data)
                     connection.close()
              listen.close()
              thread.interrupt_main()
                     
#main loop
def work(i,ip,size_of_file, filename, extension, secure_part, chunk):
       #specify host ip and port num
       serverHost = ip[i]
       serverPort = 9010
       #create a TCP socket for clients
       new_socket = socket(AF_INET, SOCK_STREAM)
       #connect to server
       try:
            new_socket.connect((serverHost, serverPort+i))
       #if you can't connect, do nothing
       except:
            new_socket.close()
            pass
       else:
            percent = int(i)*100.0 / int(size_of_file[1])
            sb.update(i)
            #get filename path
            path = '/p2p/files/' + filename + extension
            #open file to write binary
            FILE = open(path,'ab')
            while 1:
                recv_data = new_socket.recv(chunk)
                if not recv_data:
                   FILE.close()
                   #print 'File complete!'
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
temp_size_list = []
full_filename = []
#break up extensions
new_file_list = [i.split(',') for i in file_list]
#get empty off the list
new_file_list.pop()
#get files in /p2p/files
path = '/p2p/files'
dirList = os.listdir(path)
for i in range(len(new_file_list)):
       temp_filename = new_file_list[i][0]
       temp_ext = new_file_list[i][1]
       full_filename = temp_filename + temp_ext
       #check if file is in /p2p/files, if so, omit
       try:
              full_filename in dirList[i]
       except:
              temp_file_list.append(temp_filename)
              temp_ext_list.append(temp_ext)
       else:
              #create a tracker if in your directory
              alpha_file_size = create(temp_filename, temp_ext)
              #start a listening thread
              thread.start_new_thread(ListenWork,(i,alpha_file_size[0], temp_filename, temp_ext, alpha_file_size[1], alpha_file_size[2]))
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
       path = 'http://cs5550.webs.com/' + filename + '.tracker'
       f = urllib.urlopen(path)
       #read the file
       s = f.read().split('\n')
       f.close()
       #initializing lists
       ip = []
       temppart = []
       chunk_size = []
       securepart = []
       #get the list of IP's
       newlist = [i.split(',') for i in s]
       #size of file is the last entry, minus newline
       #contains size in bytes and how much to split
       size_of_file = newlist.pop()
       #print size_of_file
       #break it down - ip's and parts
       for i in range(len(newlist)):
              ip.append(newlist[i][0])
              temppart.append(newlist[i][1])
              chunk_size.append(newlist[i][2])
       for num in temppart:
              securepart.append(int(num))
       sb = ProgressBar(100)
       for i in range(int(size_of_file[1])-1):
              work(i,ip, int(size_of_file[0]), filename, extension, securepart[i], chunk_size[i])
