"""
iOS is a lot easier to do from one file. By a lot easier, I mean GMail is my version management to get code to my phone
TODO: Autogenerate this file
"""
def parse_message(message):
    tmp = message.split(b':')
    assert(len(tmp) == 2), "Expected one `:` seperator for header and body, got\n{}".format(message)
    header, body = tmp
    body = body.split(b';')
    return header, body

def parse_layout(serialized_layout):
    tmp = serialized_layout.split(b'.')
    assert(len(tmp) == 3), "Expected three values in a layout component, got\n{}".format(serialized_layout)
    return tmp

import zmq
import pyto_ui as ui

class CanvasServer:
    type_map = {
        b'b': ui.Button
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
        self.view = ui.View()
        self.view.background_color = ui.COLOR_SYSTEM_BACKGROUND

        layout = []
        for i, component in enumerate(serialized_layout) :
            _type, text, reply = parse_layout(component)
            text = text.decode()
            widget = self.type_map[_type](title=text)
            widget.size = (100, 50)
            widget.center = (self.view.width / 2, self.view.height / (len(serialized_layout) + 1) * (i))
            widget.flex = [
                ui.FLEXIBLE_TOP_MARGIN,
                ui.FLEXIBLE_BOTTOM_MARGIN,
                ui.FLEXIBLE_LEFT_MARGIN,
                ui.FLEXIBLE_RIGHT_MARGIN
            ]
            widget.action = self.on_event
            layout.append(widget)
            self.reply_map[text] = reply

        for widget in layout:
            self.view.add_subview(widget)

        self.event_loop()

    def on_event(self, sender):
        send_msg = b'cbk' + b':' + self.reply_map[sender.title]
        self.socket.send(send_msg)

    def event_loop(self):
        ui.show_view(self.view, ui.PRESENTATION_MODE_FULLSCREEN)

if __name__ == "__main__":
    CanvasServer()
