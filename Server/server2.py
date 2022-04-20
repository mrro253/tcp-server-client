import socket
import commands
import sys
import os
import tqdm

BUFF_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


class Server:
    def __init__(self, hostname, port):
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to hostname and port
        self.sock.bind((hostname, port))

        self.sock.listen()

    def evaluate(self, expression, connection):
        received = expression.split(SEPARATOR)
        operation = received[0]
        if operation == "UPLOAD":
            print("Got ", operation)
            filename = received[1]
            filesize = received[2]
            filename = os.path.basename(filename)
            filesize = int(filesize)

            # Start receiving the file from the socket
            progess = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor = 1024)
            with open(filename, "wb") as f:
                while True:
                    print("waiting")
                    bytes_read = connection.recv(BUFF_SIZE)
                    print("Received bytes")
                    if not bytes_read:
                        # Nothing received/Done
                        print("Nothing")
                        break
                    f.write(bytes_read)
                    print("Wrote")
                    progess.update(len(bytes_read))
                    print("Updated")
            return("Received")

    def run(self):
        while True:
            # Wait for request from client
            # clientAddr is Tuple of type (host, port)
            conn, addr = self.sock.accept()

            print("Request received from ", addr)

            # Send an ACK
            conn.send("Connection Established".encode())
            try:
                while True:
                    # Receive input from client
                    clientInput = conn.recv(BUFF_SIZE).decode()
                    print("Received ", clientInput)
                    try:
                        return_val = self.evaluate(clientInput, conn)
                        conn.sendall(return_val.encode())
                    except SyntaxError:
                        conn.send("Invalid expression, try again.".encode())
                        pass
            except socket.error:
                print("Unexpected error. Connection closed")
                pass
            # Close socket
            conn.shutdown(2)
            self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Err, Usage: %s [server IP] [server port]'%sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    portNum = int(sys.argv[2])
    try:
        server = Server(hostname, portNum)
    except:
        print("Error, server not created")
        sys.exit(1)
    print("Server established")
    print("Listening")
    server.run()
