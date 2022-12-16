# Script to combine two logos into one image.
#
# Based on:
# https://stackoverflow.com/a/30228308/4060282
from PIL import Image


# open images and get sizes
logo_list = ['sphinx-doc/source/logos/OFB.png',
             'sphinx-doc/source/logos/Segula_Technologies_Logo.jpg']
images = [Image.open(x) for x in logo_list]
widths, heights = zip(*(i.size for i in images))

# make heights uniform
i_hmax = heights.index(max(heights))
i_hmin = heights.index(min(heights))
reduction_factor = heights[i_hmin]/heights[i_hmax]
increase_factor = heights[i_hmax]/heights[i_hmin]
images[i_hmin] = images[i_hmin].resize(
    (round(widths[i_hmin]*increase_factor),
     round(heights[i_hmin]*increase_factor)), Image.ANTIALIAS)
widths, heights = zip(*(i.size for i in images))

# create combined image
total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height), 'WHITE')

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('sphinx-doc/source/logos/combined_logo.jpg')