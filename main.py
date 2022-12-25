from PIL import Image
import glob
import numpy as np
from scipy import spatial

MY_TEST_PHOTO = "test_photo.jpg"
LEGO_PIECE_PATH = "lego-pieces//*"

tile_paths = []
for file in glob.glob(LEGO_PIECE_PATH):
	tile_paths.append(file)

main_photo = Image.open("")

# We have a n x m input photo that we want to reshape to n' x m where n' x m' depends upon the size of our plates
# If we do not use only square base plates, we can resize by a variable amount to allow for user selection of detail

SCALE_FACTOR = 10

new_width = int(np.round(main_photo.size[0] / SCALE_FACTOR))
new_height = int(np.round(main_photo.size[1] / SCALE_FACTOR))
resized_photo = main_photo.resize((new_width, new_height))

# For calculating what the closest color each resized pixel is to the original, we will use the euclidean distance
# For efficient look up I will use a K-D Tree, because of its conduciveness for multidimensional search (here we have 3)

kdtree = spatial.KDTree()

closest_colors = np.zeros((new_width, new_height))

for i in range(new_width):
	for j in range(new_height):
		pixel = resized_photo.getpixel((i, j))  
		closest = kdtree.query(pixel)            
		closest_colors[i, j] = closest[1]        

# Now we create the final output image; we substitute each new pixel in the mosaic with the RGB color we have selected
mosaic = Image.new('RGB', resized_photo.size)


