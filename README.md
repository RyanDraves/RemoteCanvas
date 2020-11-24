# RemoteCanvas
Proof of concept idea to remotely render a GUI. Uses zmq to transmit the layout of a GUI and send callbacks

# Installation
Linux:
- `python3 -m pip install requirements.txt`
- `python3 -m pip install -e .`

iOS:
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
- You'll need to hardcode the IP of the server in your client, because this is a lightweight project and P2P is heavyweight
