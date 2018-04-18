#!/usr/bin/env python3
# author Yannick Morvan


import datetime
import argparse
import os
from os import listdir
from os.path import isfile, join
import magic
from shutil import copy2
import hashlib
import exiftool
from datetime import datetime as DateTime
import struct

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def exif_key(mime_type):
    if 'jpeg' in mime_type:
        return 'EXIF:CreateDate'
    if 'quicktime' in mime_type or 'mp4' in mime_type:
        return 'QuickTime:CreateDate'

def name_from_exif(file_path, exif_mime_type_key):
    filename, file_extension = os.path.splitext(file_path)
    exif_Executable="/usr/bin/exiftool"

    with exiftool.ExifTool() as et:
        exif = et.get_metadata(file_path)
#        print(exif)
        if exif_mime_type_key in exif:
            date_and_time = exif[exif_mime_type_key]
            parsed_date = datetime.datetime.strptime(date_and_time, '%Y:%m:%d %H:%M:%S')
            new_name = parsed_date.strftime("%Y-%m-%d-at-%Hh-%Mm-%S") + file_extension
            year = parsed_date.strftime("%Y")
            month = parsed_date.strftime("%m")
            return new_name, year, month
        else:
            return md5sum(file_path) + file_extension, None, None



def path_name(outdir, year, month, prev_fname, new_fname):
    if year is None:
        absolute_new_path_name = os.path.join(args.outdir, 'unsorted')
        absolute_new_fname = os.path.join(absolute_new_path_name, new_fname)
        return absolute_new_path_name, absolute_new_fname
    else:
        absolute_new_path_name = os.path.join(args.outdir, year, year + '-'+ month)
        absolute_new_fname = os.path.join(absolute_new_path_name, new_fname)
        return absolute_new_path_name, absolute_new_fname

def copy_rename_file(outdir, year, month, prev_fname, new_fname):
    absolute_new_path_name, absolute_new_fname = path_name(args.outdir, year, month, prev_fname, new_fname)
    absolute_new_fname = absolute_new_fname.lower()
    print('absolute_new_path_name ', absolute_new_path_name)
    print('absolute_new_path_name ', absolute_new_fname)
    # XXXXXXXXXXXX check path first, if not existYYYYYYYYYYYY then check file

    if not os.path.exists(absolute_new_path_name):
        os.makedirs(absolute_new_path_name, exist_ok=True)
    if not os.path.exists(absolute_new_fname):
        print("Copying ", prev_fname, ' to ', absolute_new_fname)
        copy2(prev_fname, absolute_new_fname)
    else:
        print("File is already there, not overwritting ", absolute_new_fname)

def main(args):
    unsorted_path = os.path.join(args.outdir, "unsorted")
    os.makedirs(unsorted_path, exist_ok=True)
    onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(args.indir)) for f in fn]
    for current_fname in onlyfiles:
        mime_type = magic.detect_from_filename(current_fname).mime_type
        if 'jpeg' in mime_type or 'quicktime' in mime_type or 'mp4' in mime_type:
            exif_mime_type_key = exif_key(mime_type);
            new_fname, year, month  = name_from_exif(current_fname, exif_mime_type_key)
            copy_rename_file(args.outdir, year, month, current_fname, new_fname)



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("indir", help="Input directory containing the pictures")
    parser.add_argument("outdir", help="Output directory containing the sorted pictures")
    args = parser.parse_args()
    main(args)
