import socket
import time
import sys
import threading

HOST = ''
PORT = 50007
connections_ips = []
connections_sockets = []
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
                        print('Connected by',addr)
                        #addr -> connections_ips


accepter_thread = threading.Thread(name='accepter', target=accepter)
#accepter_thread.setDaemon(True)
accepter_thread.start()

while close_program == False:
        
        command = input('>>')
        
        if command == 'connect':
                        
                connect_to_ip = input('connect to (IP): ')
                connect_to_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                        connect_to_socket.connect((connect_to_ip,PORT))
                except:
                        print('Error connecting to '+connect_to_ip)
                else:
                        print('Connected to '+connect_to_ip)
                        connections_ips.append(connect_to_ip)
                        connections_sockets.append(connect_to_socket)
                                
        elif command == 'exit':

                close_program = True
                print('Closing threads...')
                accepter_thread.join()
                print('All threads closed.')
