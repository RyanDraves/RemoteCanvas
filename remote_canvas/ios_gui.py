import pyto_ui as ui
from .parse import parse_layout

class Gui:
    type_map = {
        b'b': ui.Button
    }

    def __init__(self, event_cbk):
        self.reply_map = {}
        self.event_cbk = event_cbk

    def render_layout(self, serialized_layout):
        self.view = ui.View()
        self.view.background_color = ui.COLOR_SYSTEM_BACKGROUND

        layout = []
        for i, component in enumerate(serialized_layout) :
            _type, text, reply = parse_layout(component)
            text = text.decode()
            widget = Gui.type_map[_type](title=text)
            widget.size = (100, 50)
            widget.center = (self.view.width / 2, self.view.height / (len(serialized_layout) + 1) * (i + 0.5))
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

        ui.show_view(self.view, ui.PRESENTATION_MODE_FULLSCREEN)

    def on_event(self, sender):
        self.event_cbk(self.reply_map[sender.title])
