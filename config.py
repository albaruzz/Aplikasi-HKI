"""Shared configuration for app.py and eval_cifake.py.

Preprocessing and class-mapping values must stay in sync with how the model
was trained: RGB -> resize to IMG_WIDTH x IMG_HEIGHT -> optional /255 rescale,
single sigmoid output where CLASS_1 corresponds to prob >= 0.5.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "my_model21.h5")

IMG_WIDTH = 32
IMG_HEIGHT = 32
RESCALE = True

CLASS_0 = "Fake"
CLASS_1 = "Real"
