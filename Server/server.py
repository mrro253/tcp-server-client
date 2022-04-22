import socket

IP = "localhost"
PORT = 4282
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
SEPARATOR = "<SEPARATOR>"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[Listening]")
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        token = conn.recv(SIZE).decode(FORMAT)
        token = token.split(SEPARATOR)
        command = token[0]
        print("[RECV] Command received.")
        print("Command:", command)
        if (command == "UPLOAD"):
            print("upload")
            filename = token[1]
            file = open("server_data/"+filename, "w")
            conn.send("Filename received".encode(FORMAT))

            data = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] File data received.")
            file.write(data)
            conn.send("File data received.".encode(FORMAT))

            file.close()
        elif (command == "CONNECT"):
            print("Getting connect.")
            conn.send("Connection established".encode(FORMAT))
        elif command == "QUIT":
            conn.send("Connection closed.")
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected")
        else:
            print("idk")

if __name__ == "__main__":
    main()
