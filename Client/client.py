import socket
import os
import tqdm

FORMAT = "utf-8"
SIZE = 1024
SEPARATOR ="<SEPARATOR>"

def main():
    while True:
        userInput = input(">")
        userInput = userInput.split(" ")
        command = userInput[0]
        if (command == "CONNECT"):
            IP = userInput[1]
            PORT = int(userInput[2])
            ADDR = (IP, PORT)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            client.sendall(f"{command}{SEPARATOR}{IP}{SEPARATOR}{PORT}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

        if command == "DELETE":
            filename = userInput[1]
            client.sendall(f"{command}{SEPARATOR}{filename}".encode(FORMAT))
            confirmation = client.recv(SIZE).decode(FORMAT)
            print("[SERVER]: " + confirmation)

        if (command == "UPLOAD"):
            filename = userInput[1]
            filesize = os.path.getsize(filename)
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
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            file.close()

        if command == "DOWNLOAD":
            filename = userInput[1]
            client.sendall(f"{command}{SEPARATOR}{filename}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            othermsg = msg.split(SEPARATOR)
            filesize = int(othermsg[1])
            client.send("Ready to receive file".encode(FORMAT))

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor = 1024)
            recv_size = 0
            with open(filename, "wb") as f:
                while recv_size < filesize:
                    data = client.recv(SIZE)
                    if not data:
                        break
                    f.write(data)
                    progress.update(len(data))
                    recv_size += SIZE
                progress.close()

            print(f"[RECV] File data received.")
            client.send("File data received.".encode(FORMAT))
            f.close()

        if command == "DIR":
            client.send(command.encode(FORMAT))
            num_files = client.recv(SIZE).decode(FORMAT)
            client.send("Ready for DIR.".encode(FORMAT))
            for i in range(int(num_files)):
                print(client.recv(SIZE).decode(FORMAT))

        if command == "QUIT":
            client.send(command.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            client.close()
            break

if __name__ == "__main__":
    main()