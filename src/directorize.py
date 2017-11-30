import os
import re
import shutil
import sys

"""
Move files into the multidir dump structure based on their prefixes. 
"""

# Map filenames to directory names
dir_names = {'FV-hires01':'FV-hires-01'}

files = os.listdir('.')
dir_name = '%04i/%s'

for f in files:
    m = re.match('(.*)\-([\d]+)\.bob', f)

    if not m:
      continue

    dump = int(m.group(2))
    dir_prefix = dir_names.get(m.group(1), m.group(1))

    print dir_prefix

    path = dir_name % (dump, dir_prefix)

    if not os.path.exists(path):
        os.makedirs(path)

    print "Moving ", f, "to ", "%s/%s" % (path, f)
    shutil.move(f, "%s/%s" % (path, f))

