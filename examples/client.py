from RemoteCanvas.canvas.canvas_client import CanvasClient
import time

def on_explore():
    print("Exploring")

def on_solve():
    print("Solving")

def on_stop():
    print("Stopping")

if __name__ == "__main__":
    canvas = CanvasClient(server_ip = "192.168.1.123")
    canvas.register_button("Explore", on_explore)
    canvas.register_button("Solve", on_solve)
    canvas.register_button("Stop", on_stop)
    canvas.start_gui()

    while True:
        print(".")
        time.sleep(1)
