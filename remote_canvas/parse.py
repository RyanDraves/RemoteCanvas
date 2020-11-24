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
