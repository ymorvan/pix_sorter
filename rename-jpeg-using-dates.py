#!/usr/bin/env python3
# example https://gist.github.com/n3wtron/5858940
from PIL import Image
from PIL.ExifTags import TAGS
import PIL.Image
import datetime
import argparse
import os
from os import listdir
from os.path import isfile, join
import magic
from shutil import copy2
import hashlib


def get_exif(fn):
    ret = {}
    i = PIL.Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = PIL.ExifTags.TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def main(args):
    unsorted_path = os.path.join(args.outdir, "unsorted")
    os.makedirs(unsorted_path, exist_ok=True)
    onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(args.indir)) for f in fn]
    for file_path in onlyfiles:
        ftype = magic.detect_from_filename(file_path).mime_type;
        if 'jpeg' in ftype:
            print (file_path)
            exif = get_exif(file_path)
            if 'DateTimeOriginal' in exif:
                date_and_time = exif['DateTimeOriginal'];
                parsed_date = datetime.datetime.strptime(date_and_time, '%Y:%m:%d %H:%M:%S')
                new_name = parsed_date.strftime("%Y-%m-%d-at-%Hh-%Mm-%S") + ".jpg"
                year = parsed_date.strftime("%Y")
                month = parsed_date.strftime("%m")
                target_path = os.path.join(args.outdir, year, month)
                target_name = os.path.join(args.outdir, year, month, new_name)
                os.makedirs(target_path, exist_ok=True)
                copy2(file_path, target_name)
            else:
                copy2(file_path, os.path.join(unsorted_path, md5sum(file_path)) + ".jpg" )


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("indir", help="Input directory containing the pictures")
    parser.add_argument("outdir", help="Output directory containing the sorted pictures")
    args = parser.parse_args()
    main(args)
