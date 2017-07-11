import socket

HOST = ''
PORT = 50008

while True:

    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    accept_socket.bind((HOST,PORT))
    accept_socket.listen(1)

    conn, addr = accept_socket.accept()
    print('Connected by',addr)
