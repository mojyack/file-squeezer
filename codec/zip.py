import os

accept_exts = [".psd", ".clip"]

def compress(file):
    new = file + ".zip"
    return [["7z", "a", new, file]]
