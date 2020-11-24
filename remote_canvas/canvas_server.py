import zmq
import PySimpleGUI as sg
from .parse import parse_message, parse_layout

class CanvasServer:
    type_map = {
        b'b': sg.Button
    }

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:5555")

        self.reply_map = {}

        self.listen_for_layout()

    def listen_for_layout(self):
        # Handshake
        _ = self.socket.recv()
        self.socket.send(b'.')

        message = self.socket.recv()
        header, body = parse_message(message)

        if header == b'gui':
            self.render_layout(body)

    def render_layout(self, serialized_layout):
        layout = []

        for component in serialized_layout:
            _type, text, reply = parse_layout(component)
            text = text.decode()
            layout.append([self.type_map[_type](text)])
            self.reply_map[text] = reply

        self.window = sg.Window("Demo", layout)

        self.event_loop()

    def event_loop(self):
        while True:
            event, values = self.window.read()

            # End program if user closes window
            if event == sg.WIN_CLOSED:
                break

            if event in self.reply_map:
                send_msg = b'cbk' + b':' + self.reply_map[event]
                self.socket.send(send_msg)

        self.window.close()
