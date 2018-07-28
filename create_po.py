from distutils.core import setup
from glob import glob
from subprocess import call
import sys
from os.path import splitext, split

# IMPORTANT!
# You MUST have this packages installed in your system:
#     "librsvg2-bin" to use rsvg-convert command.
#     "intltool-debian" or "intltool" to use intltool-update command.

VERSION = '0.2.4'
SVG_CONVERT = 'rsvg-convert'
UPDATE = 'intltool-update'
UPDATE_DEBIAN = '/usr/share/intltool-debian/intltool-update'
# Make curlew.pot file from python source files.
py_files = " ".join(glob("modules/*.py"))
call("xgettext --keyword=_ -o po/gscrabble.pot {}".format(py_files), shell=True)
