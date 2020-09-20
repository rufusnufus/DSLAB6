# Used parts of the code from https://stackoverflow.com/a/59718871 
import socket
import sys
import time
from tqdm import tqdm
from os.path import getsize

# global variable
BUFFER_SIZE = 1024

if __name__ == "__main__":
    # split arguments
    file_name, addr, port = sys.argv[1:]
    # create socket for connecting
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    s.connect((addr, int(port)))
    # send the length of the file name
    s.send(str.encode(f'{len(file_name):03d}'))
    # send the
    s.send(str.encode(file_name))
    
    # send the file
    with open(file_name, 'rb') as f:
        # initialize the progress bar
        progress_bar = tqdm(total=getsize(file_name))
        print('file opened')
        # send file by buffer size portions of bytes
        l = f.read(BUFFER_SIZE)
        while l:
            s.send(l)
            # update the progress bar
            progress_bar.update(BUFFER_SIZE)
            l = f.read(BUFFER_SIZE)
        # close the progress bar
        progress_bar.close()
        print('Successfully sent the file')
    # close the connection
    s.close()
    print('connection closed')
