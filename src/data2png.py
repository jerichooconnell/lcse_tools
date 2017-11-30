"""
Script for converting LCSE raw movies to a series of .pngs. You need to edit this script manually... there are no command line arguments
"""

import os
from PIL import Image

__author__ = 'stou'


def main():
  # List filenames in "fortran order":
  # That is lower-left, lower-right, upper-left, upper-right
  #filenames = ["movieA/icfv2_11", 
  #             "movieC/icfv2_21",
  #             "movieB/icfv2_12",
  #             "movieD/icfv2_22"]

  filenames = ["movieA/ICF-10K-FV-dump27_fly_11", 
               "movieB/ICF-10K-FV-dump27_fly_12",
               "movieC/ICF-10K-FV-dump27_fly_21",
               "movieD/ICF-10K-FV-dump27_fly_22"]

  #filenames = ["icf-full_00", "icf-full_01",
  #             "icf-full_10", "icf-full_11"]

  # This is the filename prefix for the created pngs.
  #  (<prefix>-<frame-number>.png for example: 'icf-full-0047.png
  filename_out = 'converted/ICF-10K-FV-dump27-fly/ICF-10K-FV-dump27-fly'

  frame_dims = (1280, 1024)
  frame_dims_out = (2 * frame_dims[0],
                    2 * frame_dims[1])

  frame_size = 3 * frame_dims[0] * frame_dims[1]

  # We use the size from the first file.
  file_size = os.path.getsize(filenames[0])

  image_count = file_size / frame_size

  print "We have %i frames to convert" % image_count

  files = [(f, open(f, 'r')) for f in filenames]

  for img_ix in range(image_count):

    print "%0.2f %% (%i of %i) " % (100.0 * float(img_ix)/image_count, img_ix, image_count)  

    img_out = Image.new("RGB", frame_dims_out)

    for ix, file_in in enumerate(files):
      i = ix % 2
      j = ix / 2

      loc = (i * frame_dims[0],
             frame_dims[1] - j * frame_dims[1])

      data = file_in[1].read(frame_size)

      # We flip the image because image stuff thinks
      img_in = Image.frombytes("RGB", frame_dims, data).transpose(Image.FLIP_TOP_BOTTOM)
      img_out.paste(img_in, box=loc)

    img_out.save("%s-%04i.png" % (filename_out, img_ix))
  #  break

  for f in files:
    f[1].close()
    
if __name__ == '__main__':
  main()    
