accept_exts = [".wav"]

def compress(file):
    # wavpack -hh -x6
    return ["wavpack -y -hh".split(' ') + [file]]
