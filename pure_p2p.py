import socket
import time
import sys
import threading

HOST = ''
PORT = 50007
connections = []
close_program = False

socket.setdefaulttimeout(10)

def accepter():

        global close_program        

        accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        accept_socket.bind((HOST,PORT))
        accept_socket.listen(1)
        
        while close_program == False:

                try:
                        conn, addr = accept_socket.accept()                        
                except:
                        #print("accept() error: ",sys.exc_info()[0])
                        a=1
                else:
                        print('Connected by',addr[0])
                        connections.append((addr[0],conn))

accepter_thread = threading.Thread(name='accepter', target=accepter)
#accepter_thread.setDaemon(True)
accepter_thread.start()

while close_program == False:
        
        command = input('>>').split()
        
        if command[0] == 'connect':
                        
                connect_to_ip = command[1]
                connect_to_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                        connect_to_socket.connect((connect_to_ip,PORT))
                except:
                        print('Error connecting to '+connect_to_ip)
                else:
                        print('Connected to '+connect_to_ip)
                        connections.append((connect_to_ip,connect_to_socket))

        elif command[0] == 'say':

                if len(command) > 2:
                        
                        say_to_ip = command[1]
                        msg = command[2].encode()

                        for i in range(len(connections)):
                                if connections[i][0] == say_to_ip:
                                        connections[i][1].send(msg)
                                        
                else:
                        print('Not all the arguments provided.')
                                
        elif command[0] == 'exit':

                close_program = True
                print('Closing threads...')
                accepter_thread.join()
                print('All threads closed.')
