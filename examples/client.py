from remote_canvas.canvas_client import CanvasClient
import time
import sys

def on_explore():
    print("Exploring")

def on_solve():
    print("Solving")

def on_stop():
    print("Stopping")

if __name__ == "__main__":
    server_ip = "192.168.1.123"
    if len(sys.argv) >= 2:
        server_ip = sys.argv[1]
    canvas = CanvasClient(server_ip = server_ip)
    canvas.register_button("Explore", on_explore)
    canvas.register_button("Solve", on_solve)
    canvas.register_button("Stop", on_stop)
    canvas.start_gui()

    print("GUI started")
    while True:
        print(".")
        time.sleep(1)
