from PIL import Image
import numpy as np
from scipy import spatial
import some_class_stuff

# Settings for the script
MAKE_SQUARE = True
OUTPUT_DIMS = (62,62)

# Read the input photo, keep it
MY_TEST_PHOTO = "test_image_dubu.jpg"
input = Image.open(MY_TEST_PHOTO)
input_photo = input 

# If we are making a square mosaic we will need to crop if the image is not already a square
if input.size[0] != input.size[1]:
	# In the future this will take user input to crop the image
	# Right now we take the top left corner and drag to form a square
	width, height = input.size
	if width > height:
		input_photo = input.crop((0, 0, height, height))
	else:
		input_photo = input.crop((0, 0, width, width))

# Take cropped (or uncropped) input_photo and rescale to the desired dimensions
# SCALE_FACTOR_WIDTH = float(OUTPUT_DIMS[0] / input_photo.size[0])
# SCALE_FACTOR_HEIGHT = float(OUTPUT_DIMS[1] / input_photo.size[1])
# new_width = int(np.round(input_photo.size[0] * SCALE_FACTOR_WIDTH))
# new_height = int(np.round(input_photo.size[1] * SCALE_FACTOR_HEIGHT))
# resized_input_photo = input_photo.resize((new_width, new_height))

new_width = OUTPUT_DIMS[0]
new_height = OUTPUT_DIMS[1]
resized_input_photo = input_photo.resize((OUTPUT_DIMS[0], OUTPUT_DIMS[1]))

# For calculating what the closest color each resized pixel is to the original, we will use the euclidean distance
# For efficient look up I will use a K-D Tree, because of its conduciveness for multidimensional search (here we have 3)
colors = list(some_class_stuff.lego_color_rgb.values())
kdtree = spatial.KDTree(colors)
closest_colors_mat = np.zeros((new_width, new_height))
# output_colors_list is used to store the rgb values we are building the new image with
output_colors_list = []

for i in range(new_width):
	for j in range(new_height):
		pixel = resized_input_photo.getpixel((i, j))  
		closest_ind = int(kdtree.query(pixel)[1])
		closest_colors_mat[i, j] = closest_ind
		output_colors_list.append(list(colors[closest_ind]))

output_colors_list = [rgb_val for pxl in output_colors_list for rgb_val in pxl]
output_colors = bytes(output_colors_list)

# Now we create the final output image; we substitute each new pixel in the mosaic with the RGB color we have selected
lego_output_img = Image.frombytes("RGB", (new_width, new_height), output_colors)
lego_output_img = lego_output_img.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)
lego_output_img.show()


