#!/usr/bin/env python
import argparse
from contextlib import contextmanager
from sidomo import Container # sudo -H pip install 'git+https://github.com/deepgram/sidomo.git#egg=sidomo'
#import docker
#import dockerpty
import tempfile
import shutil
import os.path

# from http://stackoverflow.com/a/22726782/3315914
@contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)

parser = argparse.ArgumentParser(description='Generates a blend file with animations from an mhx2 file')
parser.add_argument('--mhx2', help='path to the mhx2 file')
parser.add_argument('--textures', help='path to the textures dir')
parser.add_argument('--animations', help='path to the animations zip file')
parser.add_argument('--outputfile', help='path to the blender output file')
parser.add_argument('--unpack', help='if the included files should be unpacked (recommended) default : True',default=True)

#with TemporaryDirectory() as temp_dir:
#    cp "$mhx2" "$TEMP_DIR/massis.mhx2"

args = parser.parse_args()
mhx2_dir = os.path.abspath(os.path.join(args.mhx2, os.pardir))
output_dir = os.path.abspath(os.path.join(args.outputfile, os.pardir))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if args.textures == None:
    args.textures = os.path.join(mhx2_dir,'textures')

with TemporaryDirectory() as temp_dir:
    # copy files to temp
    # mhx2
    shutil.copyfile(args.mhx2,os.path.join(temp_dir,'massis.mhx2'))
    # textures
    if os.path.exists(args.textures):
        shutil.copytree(args.textures,os.path.join(temp_dir,'textures'))
    # animations
    shutil.copyfile(args.animations,os.path.join(temp_dir,'animations.zip'))

    with Container('rpax/massis-makehuman',volumes=[temp_dir+":/media"],environment=["mhx2=/media/massis.mhx2","animations=/media/animations.zip","output=/media/output.blend"]) as c:
        for output_line in c.run('/usr/bin/run-converter'):
            print(output_line)

    if os.path.exists(os.path.join(output_dir,'textures')):
        shutil.rmtree(os.path.join(output_dir,'textures'))

    shutil.copytree(os.path.join(temp_dir,'textures'),os.path.join(output_dir,'textures'))
    shutil.copyfile(os.path.join(temp_dir,'output.blend'),args.outputfile)






#
