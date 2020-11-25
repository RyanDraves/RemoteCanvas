# RemoteCanvas
Proof of concept idea to remotely render a GUI. Uses zmq to transmit the layout of a GUI and send callbacks

# Installation
Linux:
- `python3 -m pip install requirements.txt`
- `python3 -m pip install .`

iOS:
- From some other machine, run `python3 generate_ios.py`
- Get the contents of `canvas/canvas_server_ios.py` into a file in Pyto
- You could just hit the play button to run the script, but this setup adds it to Siri
- Click the funny little gear icon in the bottom right when the file is open
- Click `Add to Siri`
- Choose a trigger phrase under "When I say"
- Under "Do," select `Run Script` -> `Show More` -> enable `Show Console`
- Click `Add to Siri`

# Usage
iOS:
- Run the server script or launch it from Siri

Linux:
- Following `examples/`, either create a server script or modify a program to be a client

# Limitations
- Haven't figured out how to get the UDP broadcast handshake through WSL2. Natively, without networking voodoo I haven't figured out, you won't be able to cross the bridge to/from WSL2. If both client/server are on WSL2, or both on different platforms, then everything will work
