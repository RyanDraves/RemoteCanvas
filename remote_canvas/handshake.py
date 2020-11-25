# Many thanks to https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5
import socket
from .constants import *
import time
import threading

def handshake_server(byzantine_cv, byzantine_event):
    # Send UDP broadcasts to establish a zmq pairing connection
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    server.bind(("", HANDSHAKE_PORT))

    cv = threading.Condition()
    event = threading.Event()  # Python shenanigans prevent using just a bool here

    client_addr = None

    while True:
        with byzantine_cv:
            if byzantine_event.is_set():
                break

        # Broadcast a SEND on the LAN
        server.sendto(MAGIC_HANDSHAKE_SEND, ('<broadcast>', HANDSHAKE_PORT))
        try:
            # Janky double receive. We're going to get our own broadcast, so the second one is the "real" receive
            data, client_addr = server.recvfrom(1024)
            if data == MAGIC_HANDSHAKE_ACK:
                break
            data, client_addr = server.recvfrom(1024)
            if data == MAGIC_HANDSHAKE_ACK:
                break
        except socket.timeout as timeout:
            pass

    server.close()

    return client_addr

def handshake_client():
    # Listen for UDP broadcasts to establish a zmq pairing connection
    # Many thanks to https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", HANDSHAKE_PORT))

    while True:
        # Receive a handshake SEND from the server, then reply with an ACK
        data, server_addr = client.recvfrom(1024)
        if data == MAGIC_HANDSHAKE_SEND:
            client.sendto(MAGIC_HANDSHAKE_ACK, server_addr)
            break

    client.close()

    return server_addr

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        print(handshake_client())
    else:
        print(handshake_server())
