import socket
import tqdm

IP = "localhost"
PORT = 4281
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
            filesize = int(token[2])
            conn.send("Filename received".encode(FORMAT))

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor = 1024)
            recv_size = 0
            with open("server_data/"+filename, "wb") as file:
                print("Waiting")
                while recv_size < filesize:
                    data = conn.recv(SIZE)
                    print("Received")
                    if not data:
                        break
                    file.write(data)
                    print("Wrote")
                    progress.update(len(data))
                    recv_size += SIZE
                progress.close()

            print(f"[RECV] File data received.")
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
