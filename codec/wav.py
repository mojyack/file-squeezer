accept_exts = [".flac"]

def compress(file):
    return ["flac -d".split(' ') + [file]]
