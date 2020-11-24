import zmq
import threading
from .parse import parse_message
import time

class CanvasClient:
    def __init__(self):
        self.context = zmq.Context()
        self.handshake_socket = self.context.socket(zmq.REQ)
        self.handshake_socket.connect("tcp://localhost:5555")
        self.event_socket = self.context.socket(zmq.SUB)
        self.event_socket.connect("tcp://localhost:5557")
        self.event_socket.setsockopt(zmq.SUBSCRIBE, b'cbk')
        self.layout_socket = self.context.socket(zmq.PUB)
        self.layout_socket.bind("tcp://*:5556")
        topic = b'gui'
        messagedata = 1
        self.layout_socket.send(b"%s %d" % (topic, messagedata))
        self.seq = 0
        self.callback_map = {}
        self.layout = []

        self.running = True

    def register_button(self, text, callback):
        self.layout.append('b.{}.{}'.format(text, self.seq).encode())
        self.callback_map[self.seq] = callback
        self.seq += 1

    def start_gui(self):
        self.handshake_socket.send(b'.')
        _ = self.handshake_socket.recv()

        data = b'gui' + b' ' + b';'.join(self.layout)
        self.layout_socket.send(data)

        recv_thread = threading.Thread(target=self.recv_events)
        recv_thread.start()

    def recv_events(self):
        while self.running:
            message = self.event_socket.recv()
            header, body = parse_message(message)
            if header == b'cbk':
                self.callback_map[int(body[0])]()
