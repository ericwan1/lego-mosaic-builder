
from PIL import Image
import glob

MY_TEST_PHOTO = "test_photo.jpg"
LEGO_PIECE_PATH = "lego-pieces//*"

tile_paths = []
for file in glob.glob(LEGO_PIECE_PATH):
	tile_paths.append(file)


