import zmq
import threading
from .parse import parse_message, parse_layout
from .constants import *
from .handshake import handshake_server
import sys
if sys.platform == "linux":
    from .linux_gui import *
elif sys.platform == "ios":
    from .ios_gui import *

class CanvasServer:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:{}".format(ZMQ_PORT))

        self.gui = Gui(self.handle_event)

        self.listen_for_layout()

    def __del__(self):
        if self.context is not None:
            self.context.term()

    def handle_event(self, reply):
        send_msg = b'cbk' + b':' + reply
        self.socket.send(send_msg)

    def listen_for_layout(self):
        byzantine_cv = threading.Condition()
        byzantine_event = threading.Event()
        threading.Thread(target=handshake_server, args=[byzantine_cv, byzantine_event]).start()

        message = self.socket.recv()
        header, body = parse_message(message)

        assert(header == b'gui'), "Expected b'gui' got {}".format(header)

        # Notify the server handshake that it can stop trying to handshake
        with byzantine_cv:
            byzantine_event.set()

        # Send an ACK to receiving the GUI
        ack_msg = b'gui' + b':' + b'ACK'
        self.socket.send(ack_msg)

        # Blocking call to render the GUI
        self.gui.render_layout(body)
