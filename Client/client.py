import socket
import os
import tqdm

IP = "localhost"
PORT = 4281
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
SEPARATOR ="<SEPARATOR>"

def main():
    while True:
        userInput = input(">")
        userInput = userInput.split(" ")
        command = userInput[0]
        print(userInput)
        if (command == "CONNECT"):
            IP = userInput[1]
            PORT = userInput[2]
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            client.sendall(f"{command}{SEPARATOR}{IP}{SEPARATOR}{PORT}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

        if (command == "UPLOAD"):
            filename = userInput[1]
            filesize = os.path.getsize(filename)
            print("Filesize: ", filesize)
            client.sendall(f"{command}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            bytes_sent = 0
            with open(filename, "rb") as file:
                while bytes_sent < filesize:
                    data = file.read(SIZE)
                    if not data:
                        break
                    client.sendall(data)
                    progress.update(len(data))
                    bytes_sent += SIZE
                progress.close()
            print("waiting after send")
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            file.close()
        if command == "QUIT":
            client.send(userInput.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            client.close()

if __name__ == "__main__":
    main()