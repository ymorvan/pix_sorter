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

def get_exif(fn):
    ret = {}
    i = PIL.Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = PIL.ExifTags.TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def main(args):
    onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(args.indir)) for f in fn]
    for file_path in onlyfiles:
        ftype = magic.detect_from_filename(file_path).mime_type;
        if 'jpeg' in ftype:
            print (file_path)
            exif = get_exif(file_path)
            if 'DateTimeOriginal' in exif:
                date_and_time = exif['DateTimeOriginal'];
                parsed_date = datetime.datetime.strptime(date_and_time, '%Y:%m:%d %H:%M:%S')
                year = '0000'# datetime.datetime.strptime(date_and_time, '%Y')
                month = 'jan' #datetime.datetime.strptime(date_and_time, '%m')
                new_name = parsed_date.strftime("%Y-%m-%d-at-%Hh-%Mm-%S")
                year = parsed_date.strftime("%Y")
                month = parsed_date.strftime("%m")
                target_path = os.path.join(args.outdir, year, month)
                print("Target " + target_path)
                print("new name " + new_name)


#for file in glob.iglob(args.indir, recursive=True):
#    print("It is ", file)

#fn = '/home/ymorvan/Pictures/usb-iphone-pics-to-be-backed-up/IMG_1230.JPG';
#
#time_and_time = a['DateTimeOriginal'];
#parsed_date=datetime.datetime.strptime(time_and_time, '%Y:%m:%d %H:%M:%S')
#new_name = parsed_date.strftime("%Y-%m-%d-%H-%M-%S")
#print(new_name + '.jpg' )

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("indir", help="Input directory containing the pictures")
    parser.add_argument("outdir", help="Output directory containing the pictures")
    args = parser.parse_args()
    main(args)
