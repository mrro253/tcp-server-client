import os
import socket
import tqdm
import time

IP = "localhost"
PORT = 4280
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
SEPARATOR = "<SEPARATOR>"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[Listening on port {PORT}]")
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        token = conn.recv(SIZE).decode(FORMAT)
        token = token.split(SEPARATOR)
        command = token[0]
        print(f"[RECV]: {command} received.")

        if command == "CONNECT":
            print("Getting connect.")
            conn.send("Connection established".encode(FORMAT))

        if command == "DELETE":
            filename = token[1]
            os.remove('server_data/' + filename)
            conn.sendall(f"{filename} successfully deleted.".encode(FORMAT))

        if command == "UPLOAD":
            filename = token[1]
            filesize = int(token[2])
            conn.send("Filename received".encode(FORMAT))

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            recv_size = 0
            with open("server_data/"+filename, "wb") as file:
                while recv_size < filesize:
                    data = conn.recv(SIZE)
                    if not data:
                        break
                    file.write(data)
                    progress.update(len(data))
                    recv_size += SIZE
                progress.close()

            print(f"[RECV] File data received.")
            conn.send("File data received.".encode(FORMAT))
            file.close()

        if command == "DOWNLOAD":
            try:
                filename = token[1]
                filesize = os.path.getsize("server_data/" + filename)
                conn.sendall(f"{filename}{SEPARATOR}{filesize}".encode(FORMAT))
                msg = conn.recv(SIZE).decode(FORMAT)
                print(f"[CLIENT]: {msg}")

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                                     unit_divisor=1024)
                bytes_sent = 0
                file = open("server_data"+filename, "rb")
            except FileNotFoundError:
                conn.send("Error".encode(FORMAT))
                continue
            else:
                while bytes_sent < filesize:
                    data = file.read(SIZE)
                    if not data:
                        break
                    conn.sendall(data)
                    progress.update(len(data))
                    bytes_sent += SIZE
                progress.close()
                msg = conn.recv(SIZE).decode(FORMAT)
                print(f"[CLIENT]: {msg}")
                file.close()

        if command == "DIR":
            files = os.listdir("server_data")
            num_files = str(len(files))
            conn.send(num_files.encode(FORMAT))
            green_light = conn.recv(SIZE).decode(FORMAT)
            for file in files:
                created_on_big = os.path.getctime("server_data/"+file)
                created_on = time.ctime(created_on_big)

                ind_size = os.path.getsize("server_data/"+file)
                msg = file + "  Size: " + str(ind_size) + " Bytes"\
                      + "  Created on: " + str(created_on) + '\n'
                conn.send(msg.encode(FORMAT))

        if command == "QUIT":
            conn.send("Connection closed.".encode(FORMAT))
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected")
            break


if __name__ == "__main__":
    main()
