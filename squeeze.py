import os
import sys
import shutil
import random
from os.path import join, islink, splitext, isdir, relpath, dirname, normpath

mods = []
basedir = ""
backupdir = ""
do_backup = True

def generate_commands(directory):
    commands = []

    for name in os.listdir(directory):
        file = join(directory, name)

        if islink(file):
            continue

        if isdir(file):
            commands += generate_commands(file)
            continue

        ext = splitext(file)[1]

        for mod in mods:
            if ext in mod.accept_exts:
                command = mod.compress(file)
                break
        else:
            continue
        
        if do_backup:
            bak = join(backupdir, relpath(file, basedir))
            os.makedirs(dirname(bak), exist_ok=True)
            command.append(["mv", file, bak])
        else:
            command.append(["rm", "-f", file])

        commands.append(command)

    return commands

def run_commands(commands, jobs):
    import multiprocessing
    import threading
    import subprocess

    lock = threading.Lock()
    index = 0
    def run():
        nonlocal index
        while True:
            lock.acquire()
            if index == len(commands):
                lock.release()
                break
            i = index
            index += 1
            lock.release()
    
            print(f"\033[F{i + 1}/{len(commands)}\033[K")
            for c in commands[i]:
                r = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if r.returncode != 0:
                    print(f"[Error] Job {i + 1} \"{c}\" returned {r.returncode}: ", r.stdout.decode('utf-8'))
                    break

    for a in range(jobs if jobs != None else multiprocessing.cpu_count()):
        threading.Thread(target=run).start()

enable_jxl = True
enable_wavpack = True
enable_webp = False
enable_wav = False
enable_zip = True
enable_flac2wv = False

jobs = None
for arg in sys.argv[1:]:
    if arg == "-d":
        do_backup = False
    elif arg.startswith("-j"):
        jobs = int(arg[2:])
    elif arg.startswith("-m"):
        arg = "," + arg[2:] + ","
        enable_jxl = ",jxl," in arg
        enable_wavpack = ",wv," in arg
        enable_webp = ",webp," in arg
        enable_wav = ",wav," in arg
        enable_zip = ",zip," in arg
        enable_flac2wv = ",flac2wv," in arg
    else:
        basedir = arg

if len(basedir) == 0:
    print("please specify target directory")
    exit(1)

if enable_jxl:
    from codec import jxl
    mods.append(jxl)
if enable_wavpack:
    from codec import wavpack
    mods.append(wavpack)
if enable_webp:
    from codec import webp
    mods.append(webp)
if enable_wav:
    from codec import wav
    mods.append(wav)
if enable_zip:
    from codec import zip
    mods.append(zip)
if enable_flac2wv:
    from codec import flac2wv
    mods.append(flac2wv)

basedir = normpath(basedir)
backupdir = basedir + ".old"

commands = generate_commands(basedir)
random.shuffle(commands)
run_commands(commands, jobs)
