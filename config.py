import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "my_model21.h5")

IMG_WIDTH = 32
IMG_HEIGHT = 32
RESCALE = True

CLASS_0 = "Fake"
CLASS_1 = "Real"
