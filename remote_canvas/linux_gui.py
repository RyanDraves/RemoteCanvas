import PySimpleGUI as sg
from .parse import parse_layout

class Gui:
    type_map = {
        b'b': sg.Button
    }

    def __init__(self, event_cbk):
        self.reply_map = {}
        self.event_cbk = event_cbk

    def render_layout(self, serialized_layout):
        layout = []

        for component in serialized_layout:
            _type, text, reply = parse_layout(component)
            text = text.decode()
            layout.append([Gui.type_map[_type](text)])
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
                self.event_cbk(self.reply_map[event])

        self.window.close()
