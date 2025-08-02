import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.40", 11550))  # set this to your esp32c3 address

while True:
    print("send on")
    s.sendall(b"on\n")
    time.sleep(0.25)
    print("send off")
    s.sendall(b"off\n")
    time.sleep(0.25)

# s.sendall(b"abdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

# print("Got:", s.recv(64))
s.close()
