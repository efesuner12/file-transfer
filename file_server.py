import socket
import tqdm
import os

HOST = "0.0.0.0"
PORT = 5001
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 15000

s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)
print(f"[*] Listening as {HOST}:{PORT}")

client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

# receive the file infos
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
finalfilename = "server_data\\received_" + filename
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)

with open(finalfilename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break

        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

client_socket.close()
s.close()
