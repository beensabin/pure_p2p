import socket
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
            a=1
        else:
            connections.append((conn,addr))
            print('Connected by',addr)

accepter_t = threading.Thread(name='accepter', target=accepter)
accepter_t.start()

while close_program == False:

    command = input()

    if command == 'exit':
        
        close_program = True
        print('Closing accepter...')
        accepter_t.join()
