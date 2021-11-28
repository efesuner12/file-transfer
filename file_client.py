import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 15000 # send 4096 bytes each time step
PORT = 5001
#add your files in this directory
FILENAME = "source\\data.png"
FILESIZE = os.path.getsize(FILENAME)

s = socket.socket()
print(f"[+] Connecting to {socket.gethostname()}:{PORT}")
s.connect((socket.gethostname(), PORT))
print("[+] Connected.")

s.send(f"{FILENAME}{SEPARATOR}{FILESIZE}".encode())

progress = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit = "B", unit_scale = True, unit_divisor = 1024)

with open(FILENAME, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        # we use sendall to assure transimission in busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

s.close()
