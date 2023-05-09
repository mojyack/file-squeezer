from os.path import splitext
from threading import Lock

accept_exts = [".flac"]

lock = Lock()
count = 0

def compress(file):
    global lock
    global count

    with lock:
        tmp = f"/tmp/sq-{count}.wav"
        count += 1

    new = splitext(file)[0] + '.wv'
    
    # wavpack -hh -x6
    return [["flac", "-d", "-o", tmp, file], 
            ["wavpack", "-y", "-hh", "-o", new, tmp],
            ["rm", tmp]]
