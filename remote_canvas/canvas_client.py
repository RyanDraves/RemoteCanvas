import zmq
import threading
from .parse import parse_message
from .constants import *
from .handshake import handshake_client

class CanvasClient:
    def __init__(self):
        self.context = None

        self.seq = 0
        self.callback_map = {}
        self.layout = []

        self.running = True

    def __del__(self):
        if self.context is not None:
            self.context.term()

    def register_button(self, text, callback):
        self.layout.append('b.{}.{}'.format(text, self.seq).encode())
        self.callback_map[self.seq] = callback
        self.seq += 1

    def start_gui(self):
        server_addr = handshake_client()
        print("Handshake complete with server {}".format(server_addr[0]))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://{}:{}".format(server_addr[0], ZMQ_PORT))

        # Sometimes the first message or so fails, so send the layout until an ACK is received
        while True:
            data = b'gui' + b':' + b';'.join(self.layout)
            self.socket.send(data)
            
            reply = self.socket.poll(timeout=1000)
            if reply:
                message = self.socket.recv()
                header, body = parse_message(message)
                if header == b'gui' and body[0] == b'ACK':
                    break

        recv_thread = threading.Thread(target=self.recv_events)
        recv_thread.start()

    def recv_events(self):
        while self.running:
            message = self.socket.recv()
            header, body = parse_message(message)
            if header == b'cbk':
                self.callback_map[int(body[0])]()
