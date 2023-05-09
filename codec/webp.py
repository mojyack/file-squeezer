import os

accept_exts = [".png"]

def compress(file):
    new = os.path.splitext(file)[0] + ".webp"
    return ["cwebp -lossless -z 9 -o".split(' ') + [new, file]]
