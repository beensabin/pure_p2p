import socket
import time
import sys
import threading

def main():
	
        HOST = ''
        PORT = 50007

        #socket.setdefaulttimeout(10)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        s.listen(1)
        try:
                conn, addr = s.accept()
        except:
                print("accept() error: ",sys.exc_info()[0])
        else:
                print ('Connected by',addr)

                while 1:
                        data = conn.recv(1024).decode()
                        if not data or data == 'close': break
                        print(data)
                
	
if __name__ == "__main__":
	main()
