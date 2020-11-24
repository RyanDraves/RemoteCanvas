import zmq
import threading
from .parse import parse_message
import time

class CanvasClient:
    def __init__(self, server_ip):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://{}:5555".format(server_ip))

        self.seq = 0
        self.callback_map = {}
        self.layout = []

        self.running = True

    def register_button(self, text, callback):
        self.layout.append('b.{}.{}'.format(text, self.seq).encode())
        self.callback_map[self.seq] = callback
        self.seq += 1

    def start_gui(self):
        # Handshake
        self.socket.send(b'.')
        _ = self.socket.recv()

        data = b'gui' + b':' + b';'.join(self.layout)
        self.socket.send(data)

        recv_thread = threading.Thread(target=self.recv_events)
        recv_thread.start()

    def recv_events(self):
        while self.running:
            message = self.socket.recv()
            header, body = parse_message(message)
            if header == b'cbk':
                self.callback_map[int(body[0])]()
