import json

def add_file(data, filename, info, is_main):
    with open(filename) as fp:
        new_data = fp.read()
    
    for ban in info["ban"]:
        new_data = new_data.replace(ban, "")

    if not is_main:
        index = new_data.find('if __name__ == "__main__":')
        if index >= 0:
            new_data = new_data[:index]
    
    return data + new_data


with open("ios_gen.json") as fp:
    gen_info = json.load(fp)

data = '"""\n\
iOS is a lot easier to do from one file. By a lot easier, I mean GMail is my version management to get code to my phone\n\
"""\n'

for i, keyval in enumerate(gen_info.items()):
    filename, info = keyval
    data = add_file(data, filename, info, i == len(gen_info))

data += '\nif __name__ == "__main__":\n\
    server = CanvasServer()\n'

with open("remote_canvas/canvas_server_ios.py", 'w') as fp:
    fp.write(data)
