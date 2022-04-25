import socket
import os
import tqdm

FORMAT = "utf-8"
SIZE = 1024
SEPARATOR ="<SEPARATOR>"

def main():
    isConnected = False
    while True:
        userInput = input(">")
        userInput = userInput.split(" ")
        command = userInput[0]

        if (command == "CONNECT"):
            isConnected = True
            IP = userInput[1]
            PORT = int(userInput[2])
            ADDR = (IP, PORT)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            client.sendall(f"{command}{SEPARATOR}{IP}{SEPARATOR}{PORT}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

        if command == "DELETE":
            if not isConnected:
                print("[Error]: Not connected to a server. Usage: CONNECT <IP> <PORT>")
                continue
            filename = userInput[1]
            client.sendall(f"{command}{SEPARATOR}{filename}".encode(FORMAT))
            confirmation = client.recv(SIZE).decode(FORMAT)
            print("[SERVER]: " + confirmation)

        if (command == "UPLOAD"):
            if not isConnected:
                print("[Error]: Not connected to a server. Usage: CONNECT <IP> <PORT>")
                continue
            if len(userInput) != 2:
                print("[Error]: Usage: UPLOAD <filename>")
                continue
            try:
                filename = userInput[1]
                filesize = os.path.getsize(filename)
                client.sendall(f"{command}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER]: {msg}")

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                                     unit_divisor=1024)
                bytes_sent = 0
                file = open(filename, "rb")
            except FileNotFoundError:
                print("[Error]: File not found, ensure your file is in Client directory.")
                continue
            else:
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
            if not isConnected:
                print("[Error]: Not connected to a server. Usage: CONNECT <IP> <PORT>")
                continue
            if len(userInput) != 2:
                print("[Error]: Usage: UPLOAD <filename>")
                continue
            filename = userInput[1]
            client.sendall(f"{command}{SEPARATOR}{filename}".encode())
            msg = client.recv(SIZE).decode(FORMAT)
            if msg == "Error":
                print("[Error]: File does not exist.")
                continue
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
            if not isConnected:
                print("[Error]: Not connected to a server. Usage: CONNECT <IP> <PORT>")
                continue
            client.send(command.encode(FORMAT))
            num_files = client.recv(SIZE).decode(FORMAT)
            client.send("Ready for DIR.".encode(FORMAT))
            for i in range(int(num_files)):
                print(client.recv(SIZE).decode(FORMAT))

        if command == "QUIT":
            if not isConnected:
                print("[Error]: Not connected to a server. Usage: CONNECT <IP> <PORT>")
                continue
            client.send(command.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            client.close()
            isConnected = False
            break

if __name__ == "__main__":
    main()