# Used parts of the code from https://stackoverflow.com/a/59718871 
import socket
from threading import Thread
import os

# Global variables
TCP_IP = ''
TCP_PORT = 9001
BUFFER_SIZE = 1024

# thread to listen client
class ClientThread(Thread):

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(f'New thread started for {ip} : {str(port)}')

    def run(self):
        # get the length of file name
        file_len = int(self.sock.recv(3).decode())
        print('File name length is recieved')
        # get the file name
        file_name = self.sock.recv(file_len).decode()
        print('File name is recieved')
        print(file_name)

        # list of files in the directory
        files = os.listdir('.') 
        # if such file name is in directory change
        if file_name in files:
            i = 1
            parts = file_name.split('.') 
            name, ext = parts[0], '.'.join(parts[1:]) 
            while file_name in files:
                # change filename
                file_name = f'{name}_copy{i}.{ext}' 
                i += 1

        # open the file for writing data
        with open(file_name, 'wb') as f:
            # writing data to file recieving data by buffer size bytes
            while True:
                data = self.sock.recv(BUFFER_SIZE)
                if not data:
                    f.close()
                    print('file close()')
                    break
                # write data to a file
                f.write(data)

if __name__ == "__main__":
    # AF_INET – IPv4, SOCK_STREAM – TCP
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at port
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        tcpsock.listen()
        print("Waiting for incoming connections...")
        (conn, (ip, port)) = tcpsock.accept()
        print('Got connection from ', (ip, port))
        # start new thread for client
        newthread = ClientThread(ip, port, conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()