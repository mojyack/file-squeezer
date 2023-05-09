import os

accept_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

def compress(file):
    new = os.path.splitext(file)[0] + ".jxl"
    return ["cjxl -e 9 -E 3 -I 1 -q 100 --keep_invisible=0 --num_threads=0 -j 1".split(' ') + [file, new]]
