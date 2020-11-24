#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

from ..canvas.canvas_server import CanvasServer

if __name__ == "__main__":
    server = CanvasServer()
