#!/usr/bin/env python3

import os, sys
import argparse
from pydub import AudioSegment
import ffmpeg

def main():
    parser = argparse.ArgumentParser(description="Convert an audio file to raw or wav (default) format.")
    parser.add_argument("file")
    conversion_group = parser.add_mutually_exclusive_group()
    conversion_group.add_argument("-r", "--raw", 
        action="store_true",
        help="Convert to raw file")
    conversion_group.add_argument("-w", "--wav",
        action="store_true",
        help="Convert to wav")
    args = parser.parse_args()

    # change working directory as necessary
    wkdir = args.file.split('/')[:-1]
    wkdir = '/'.join(wkdir) 
    if wkdir:
        os.chdir(wkdir)

    # extract file path
    file_name = args.file.split('/')[-1]
    file_path = os.path.join(os.getcwd(), file_name)
    if not os.path.isfile(file_path):
        print(f"File '{file_name}' does not exist", file=sys.stderr)
        sys.exit(1)

    # determine format to convert from, default raw
    if len(file_name.split('.')) > 1:
        format_from = file_name.split('.')[-1]
    else:
        format_from = "raw"

    # determine format to convert to, default wav
    format_to = "wav"
    if args.raw:
        format_to = "raw"
    if args.wav:
        format_to = "wav"
    
    print(f"Converting {file_name} from .{format_from} to .{format_to}")
    sound = AudioSegment.from_file((file_path), format=format_from)
    new_name = file_name.split(".")[0] + "." + format_to
    new_path = os.path.join(os.getcwd(), new_name)
    file_handle = sound.export(new_path, format=format_to)
    print("File converted")


if __name__ == "__main__":
    main()
