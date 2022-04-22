import socket

IP = "localhost"
PORT = 4282
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
            file = open(userInput[1], "r")
            data = file.read()

            client.sendall(f"{command}{SEPARATOR}{userInput[1]}".encode())

            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

            client.send(data.encode(FORMAT))
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