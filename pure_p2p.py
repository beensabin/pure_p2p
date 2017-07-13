import socket
import time
import sys
import threading

#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = ''
PORT = 50007
connections = []
recv_threads = []
close_program = False
connected_to_server = False

socket.setdefaulttimeout(8)

accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_to_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connect_to_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

connect_to_socket.bind(('',PORT))
accept_socket.bind(('',PORT))
c_socket.bind(('',PORT))

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
        global accept_socket

        accept_socket.listen(5)
        
        already_connected = False
        
        while close_program == False:

                try:
                        conn, addr = accept_socket.accept()                        
                except:
                        pass
                else:
                        print('Connected by',addr+' (accepter thread)')

                        exists = False

                        for i in connections:
                                if i[0] == addr[0]:
                                        exists = True

                        if exists == False:
                                connections.append((addr[0],conn))
                                recv_thread = threading.Thread(target=recver, args=(addr[0],addr[1],conn,))
                                recv_thread.start()
                                recv_threads.append(recv_thread)
        

#accepter_thread = threading.Thread(name='accepter', target=accepter)
#accepter_thread.start()

connected_to_server = True

while close_program == False:

        command = input().split()

        if len(command) > 0:
        
                if command[0] == 'connect_server':

                        port = 0

                        if len(command) == 3:
                                port = int(command[2])
                        elif len(command) == 2:
                                port = PORT

                        if port != 0:
                                
                                connect_to_ip = command[1]

                                try:
                                        connect_to_socket.connect((connect_to_ip,port))
                                except Exception as e:
                                        print('Error connecting to '+connect_to_ip+': '+str(e))
                                else:
                                        print('Connected to '+connect_to_ip)
                                        connections.append((connect_to_ip,connect_to_socket))                                
                                        connected_to_server = True                                
                        else:
                                print('Command arguments error.')

                elif command[0] == 'connect':

                        port = 0

                        if len(command) == 3:
                                port = int(command[2])

                        if port != 0:
                                        
                                connect_to_ip = command[1]
                                cont = 0

                                while cont <= 10:

                                        print('Trying to connect to '+connect_to_ip+' (Attempt '+str(cont)+' of 10)')
                                        try:
                                                c_socket.connect((connect_to_ip,port))
                                        except Exception as e:
                                                print('Error connecting to '+connect_to_ip+': '+str(e))
                                        else:
                                                print('Connected to '+connect_to_ip+' (connect command)')
                                                exists = False
                                                        
                                                for i in connections:
                                                        if i[0] == connect_to_ip:
                                                                exists = True

                                                if exists == False:
                                                        connections.append((connect_to_ip,c_socket))
                                                        recv_thread = threading.Thread(target=recver, args=(connect_to_ip,port,c_socket,))
                                                        recv_thread.start()
                                                        recv_threads.append(recv_thread)

                                                cont = 12

                                        cont = cont + 1
                                        time.sleep(20)
                                        
                        else:
                                print('Command arguments error.')
                                
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
                        
                        #accepter_thread.join()
                        for r in recv_threads:
                                r.join()
                                
                        print('All threads closed.')
