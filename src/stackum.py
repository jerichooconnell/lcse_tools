
import os
from lcse_tools import image_util as iu
from PIL import Image, ImageFont, ImageDraw

#from matplotlib.font_manager import FontProperties
#matplotlib.pyplot.close("all")

fv_vars = ['FV-hires-01-back', 'FV-hires-01-front', 'FV-hires-01-slice_1', 'FV-hires-01-slice_3']
enuc_vars = ['Lg10ENUCbyP-back', 'Lg10ENUCbyP-front', 'Lg10ENUCbyP-slice_1', 'Lg10ENUCbyP-slice_3',]
out_vars = ['fv-enuc_back', 'fv-enuc_front', 'fv-enuc_slice_1', 'fv-enuc_slice_3']

def composite_fv_and_enuc(base_path, stacked_path, output_path):

    if not os.path.exists(base_path) and not os.path.exists(stacked_path):
        return

    try:
        image_a = Image.open(base_path).convert("RGBA")
        image_b = Image.open(stacked_path).convert("RGBA")
    except IOError as e:
        print e
        return

    # Crop
    image_a = iu.square_crop(image_a, image_a.size[1])
    image_b = iu.square_crop(image_b, image_b.size[1])

    # Make the second image transparent
    image_b = iu.color_to_alpha(image_b, threshold=60)
    image_a = iu.alpha_composite(image_b, image_a)

    image_a.save(output_path)
    return image_a


def stack_sets(data_path, fv_vars, enuc_vars, out_vars, dumps):

    for fv, enuc, out in zip(fv_vars, enuc_vars, out_vars):

        output_path = os.path.join(data_path, out)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        for dump in dumps:
            fv_filename = os.path.join(data_path, "%s/%s-%04i.png" % (fv, fv, dump))
            enuc_filename = os.path.join(data_path, "%s/%s-%04i.png" % (enuc, enuc, dump))
            out_filename = os.path.join(output_path, "%s-%04i.png" % (out, dump))

            if os.path.exists(out_filename):
                continue

            im = composite_fv_and_enuc(fv_filename, enuc_filename, out_filename)

            if im is not None:
              print "Wrote ", out_filename



def main():

  import sys

  data_path = sys.argv[1]

  print "data path is ", data_path

  stack_sets(data_path, fv_vars, enuc_vars, out_vars, range(3000))


if __name__ == '__main__':
  main()


