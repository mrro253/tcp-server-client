import socket
import sys
import os
import tqdm

BUFF_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

class Client:
    def __init__(self, server, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))

    def Request(self, request):

        # Send request
        self.socket.sendall(request.encode())
        # Get response
        return self.socket.recv(BUFF_SIZE).decode()

    def Upload(self, data, request):
        filename = data[1]
        filesize = os.path.getsize(filename)
        self.socket.sendall(f"{request}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFF_SIZE)
                if not bytes_read:
                    # Done
                    break
                self.socket.sendall(bytes_read)
                progress.update(len(bytes_read))

    def close(self):
        self.socket.send('\r\n')

if __name__ == '__main__':
    is_connected = False
    while not is_connected:
        data = input("> ")
        data = data.split(" ")
        request = data[0]
        if request == "CONNECT":
            hostname = data[1]
            port = int(data[2])
            try:
                client = Client(hostname, port)
                is_connected = True
            except:
                print("Connection Broken")
        else:
            print("Error: Not connected to sever, use CONNECT [IP] [Port] to use.")
    while True:
        data = input("> ")
        data = data.split(" ")
        request = data[0]
        if request == "quit":
            client.close()
            print("Connection Closed")
            exit(0)
        elif request == "UPLOAD":
            is_received = False
            while not is_received:
                client.Upload(data, request)
                status = client.socket.recv(BUFF_SIZE)
                if status == "Received":
                    is_received = True
        else:
            print("Error: Command not recognized, please try again")
        # except:
        #     print("Connection Broken")
        #     exit(1)