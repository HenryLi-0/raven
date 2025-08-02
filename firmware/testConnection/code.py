print("Hello World!")

import board
import digitalio

pin = digitalio.DigitalInOut(board.D10)
pin.direction = digitalio.Direction.OUTPUT
pin.value = False

import wifi, socketpool, time

print("board ip:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.setblocking(True)
server.bind(("0.0.0.0", 11550))
server.listen(1)
print("listening on port 11550")

buffer = bytearray(64)
while True:
    client, addr = server.accept()
    print("sent from", addr)
    client.settimeout(3)
    while True:
        try:
            num = client.recv_into(buffer)
            if num:
                msg = buffer[:num].decode("utf-8").strip()
                print("received:", msg)
                # client.send(f"ACK: {msg}\n".encode("utf-8"))
                if msg == "on":
                    pin.value = True
                elif msg == "off":
                    pin.value = False
            else:
                client.close()
                break
            time.sleep(0.1)
        except:
            print("womp womp")
            client.close()
            break



            