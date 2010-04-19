import os
import sys
from socket import *
import thread
import urllib
import random

#this function updates the gui
def update_gui(part, total):
    if total == 0:
        print('File Complete!\n')
    else:
        #calculate the percenter
        percent = part * 100.0 / total
        #if you've finished, let 'em know
        if (percent >= 99):
            sys.stdout.write('File Complete!\n')
            sys.stdout.flush()
        #if not, write out percents!
        else:
            sys.stdout.write(str(percent) + '%')
            sys.stdout.write('\b' * 15)
            sys.stdout.flush()

#create the /p2p/files directory
def p2p_dir():
    #get username
    username = os.getlogin()
    #make path
    path = '/home/' + username + '/p2p/files'
    #if the directory doesn't exist..
    if not os.path.exists(path):
        #create it!
        os.makedirs(path)
    #check again for trackers
    path = '/home/' + username + '/p2p/trackers'
    if not os.path.exists(path):
        os.makedirs(path)
        
#create a tracker
def create(filename, extension):
    #find out username
    username = os.getlogin()
    #get path for tracker
    tracker_path = '/home/' + username + '/p2p/trackers/' + filename + '.tracker'
    #get path for files
    file_path = '/home/' + username + '/p2p/files/' + filename + '.' + extension
    #get file size from file path
    file_size = os.path.getsize(file_path)
    #chunk up file to 512000 bytes a piece (500KB)
    new = file_size/512000
    #get remainder
    rem = file_size%512000
    #open file for writing the tracker to
    FILE = open(tracker_path,'w')
    #find my IP out
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('www.google.com',80))
    my_ip = s.getsockname()
    #close the socket
    s.close()
    #start writing
    for i in range(new):
        s = socket(AF_INET, SOCK_STREAM)
        randPort = random.randrange(2000,10000)
        running = 1
        while running:
            try:
                #trying to bind, if it's unsucessful, generate new port and try again
                s.bind(('',randPort))
            except:
                #generating new port
                randPort = random.randrange(2000,10000)
            else:
                #if it's successful, start new listening thread
                thread.start_new_thread(listen,(s, filename, extension, i, 512000))
                #stop while loop
                running = 0
                #write the contents to the file
                FILE.write(str(my_ip[0])+','+str(i)+','+'512000,'+str(randPort)+'\n')
    #generate new random port
    randPort = random.randrange(2000,10000)
    #while variable
    running = 1
    #opening socket for threaded listening
    new_s = socket(AF_INET, SOCK_STREAM)
    while running:
        try:
            #trying to bind, if it's unsucessful, generate new port and try again
            new_s.bind(('',randPort))
        except:
            #generating new port
            randPort = random.randrange(2000,10000)
        else:
            #if it's successful, start new listening thread
            thread.start_new_thread(listen,(new_s,filename, extension, new, rem))
            #stop while loop
            running = 0
            #write the contents to the file
            FILE.write(str(my_ip[0])+','+str(new)+','+str(rem)+','+str(randPort)+'\n')
    #FILE.write(str(file_size)+','+str(new)) <-- ditching this for now
    #close file up
    FILE.close()
#update the file list to include your files
def update_file_list():
    #variables
    full_filename = []
    #open file list
    file_list_url = urllib.urlopen('http://cs5550.webs.com/file_list')
    #find out what is in this list
    file_list = file_list_url.read().split('\n')
    #get files and extensions seperate
    combined_list = [i.split(',') for i in file_list]
    #get last blank entry out
    combined_list.pop()
    combined_list.pop()
    #-------------------------------------------
    #for whatever files are in /home/user/p2p/files
    #compare with file_list online
    #update file list online if necessary
    #-------------------------------------------
    #get username
    username = os.getlogin()
    #open file for new file list
    path = '/home/' + username + '/p2p/file_list'
    FILE = open(path, 'w')
    #get path
    file_list_path = '/home/' + username + '/p2p/files'
    #fill up directory list
    dirList = os.listdir(file_list_path)
    for i in range(len(combined_list)):
        #temporary variables
        filename = combined_list[i][0]
        extension = combined_list[i][1]
        full_filename.append(filename + extension)
    for i in range(len(dirList)):
        #check if this file is on the online file
        if dirList[i] in full_filename:
            pass
        else:
            newstr = str(dirList[i]) + '\n'
            FILE.write(newstr)
    FILE.close()
    #if your the first person to have this file, write a tracker and broadcast
    

def display_files():
    #variables
    full_filename = []
    new_list = []
    #open file list
    file_list_url = urllib.urlopen('http://cs5550.webs.com/file_list')
    #find out what is in this list
    file_list = file_list_url.read().split('\n')
    #get files and extensions seperate
    combined_list = [i.split(',') for i in file_list]
    #get last blank entry out
    combined_list.pop()
    combined_list.pop()
    #-------------------------------------
    #compare whatever is in /home/user/p2p/files
    #with whats online
    #if something is online that you don't have
    #in your files, display it for download
    #-------------------------------------
    #get username
    username = os.getlogin()
    #get path
    file_list_path = '/home/' + username + '/p2p/files'
    #fill up directory list
    dirList = os.listdir(file_list_path)
    #combine entries and throw in new list
    for i in range(len(combined_list)):
        #temporary variables
        filename = combined_list[i][0]
        extension = combined_list[i][1]
        full_filename.append(filename + extension)
    #start counter
    i = 1
    #print initial display
    print('List of files')
    print('-------------')
    #compare and display
    for filename in full_filename:
        if filename in dirList:
            pass
        else:
            new_list.append(filename)
            print '%d: %s' % (i, filename)
            i += 1
    return new_list

def tracker(filename):
    #create new path for tracker
    tracker_path = 'http://cs5550.webs.com/' + filename + '.tracker'
    #open the trackers url
    tracker_url = urllib.urlopen(tracker_path)
    #read in the web page (tracker) and split by newline
    pre_tracker_info = tracker_url.read().split('\n')
    #close url
    tracker_url.close()
    #parse up pre_tracker list
    tracker_info = [i.split(',') for i in pre_tracker_info]
    #size of file is the last entry, minus newline
    tracker_info.pop()
    #initialize lists
    ip = []
    part = []
    size = []
    port = []
    #print tracker_info
    #break down tracker_info
    for i in range(len(tracker_info)):
        ip.append(tracker_info[i][0])
        part.append(int(tracker_info[i][1]))
        size.append(int(tracker_info[i][2]))
        port.append(int(tracker_info[i][3]))
    #return a giant list of stuff
    return [ip, part, size, port]

def listen(new_socket, filename, extension, part, size):
    #keep listening on the port even after a connection and download
    while 1:
        #listen on the random port
        new_socket.listen(1)
        #accept incoming connections
        connection, address = new_socket.accept()
        full_filename = filename + '.' + extension
        #get username
        username = os.getlogin()
        #fully qualify path
        file_path = '/home/' + username + '/p2p/files/' + full_filename
        #open the file for reading
        FILE = open(file_path, 'rb')
        #read the desired parts
        FILE.seek(part * 512000)
        #set up data buffer for sending data
        send_data = FILE.read(size)
        #close up file
        FILE.close()
        #send out your data
        connection.send(send_data)
    #stop thread
    thread.interrupt_main()

def populate(filename, extension, ip, part, size, port, total):
    full_filename = filename + extension
    #get username
    username = os.getlogin()
    #fully qualify path
    file_path = '/home/' + username + '/p2p/files/' + full_filename
    #make new socket for connecting to
    new_socket = socket(AF_INET, SOCK_STREAM)
    try:
        #connect to the ip and port
        new_socket.connect((ip, port))
    except:
        print "Couldn't connect to client."
    else:
        #open up file if connect was successful
        FILE = open(file_path,'ab')
        #set up receiving data buffer
        while 1:
            #get data from socket
            recv_data = new_socket.recv(size)
            #if you're not receiving anymore bytes..
            if not recv_data:
                #close up the file
                FILE.close()
                #update the gui
                update_gui(part, total)
                #break out of the loop
                break
            #if you're recieving parts still
            else:
                #write to the file 
                FILE.write(recv_data)
    #close up socket
    new_socket.close()
    
#make necessary directories
p2p_dir()
#update the file list for peers
update_file_list()
#get username
username = os.getlogin()
#-------------------------------
#get list of files
#create trackers for all of them
#listen on all the ports as well
#-------------------------------
files_path = '/home/' + username + '/p2p/files'
dirList = os.listdir(files_path)
#list for temporary storage
newlist = []
if len(dirList) != 0:
    for files in dirList:
        file_list = files.split('.')
        create(file_list[0], file_list[1])
while 1:
    #empty file_list for re-initialization
    file_list = []
    #display the files and get a list of all files back
    file_list = display_files()
    #ask for input
    user_choice = input('Which file would you like to download (0 to quit): ')
    #if they want to exit...
    if user_choice == 0:
        print 'Exiting...'
        break
    #get filename and extension from user choice
    filename = file_list[user_choice-1][0]
    print filename
    extension = file_list[user_choice-1][1]
    #open and read the tracker
    #in the format:
    #[0] = ip_list, [1] = part_list,
    #[2] = size_list, [3] = port_list
    tracker_stuff = tracker(filename)
    #get a total (last entry in part_list in tracker_stuff)
    total = tracker_stuff[1][-1]
    #for as many parts as you have...
    for i in range(len(tracker_stuff[1])):
        #populate the file given all the info in the tracker!
        populate(filename, extension, tracker_stuff[0][i], tracker_stuff[1][i],
                 tracker_stuff[2][i], tracker_stuff[3][i], total)
