import socket
import time
import sys
import threading

HOST = ''
PORT = 50007
connections = []
recv_threads = []
close_program = False

socket.setdefaulttimeout(10)

def recver(ip,port,socket):

        global close_program

        while close_program == False:

                try:
                        recv_msg = socket.recv(1024).decode()
                except:
                        a=1
                else:
                        print('['+ip+':'+str(port)+']: '+recv_msg)

def accepter():

        global close_program
        global recv_threads

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
                        connections.append((addr[0],conn))
                        recv_thread = threading.Thread(target=recver, args=(addr[0],addr[1],conn,))
                        recv_thread.start()
                        recv_threads.append(recv_thread)
        
                        
accepter_thread = threading.Thread(name='accepter', target=accepter)
#accepter_thread.setDaemon(True)
accepter_thread.start()

while close_program == False:
        
        command = input().split()
        
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
                        recv_thread = threading.Thread(target=recver, args=(connect_to_ip,PORT,connect_to_socket,))
                        recv_thread.start()
                        recv_threads.append(recv_thread)

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
                for r in recv_threads:
                        r.join()
                        
                print('All threads closed.')
