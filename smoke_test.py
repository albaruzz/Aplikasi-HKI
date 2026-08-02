"""Smoke tests for the Flask app (stdlib unittest).

Run with: .\\.venv\\Scripts\\python.exe smoke_test.py
Note: importing `app` loads TensorFlow, so the suite takes a few seconds.
The predict test exercises lazy model loading.
"""

import io
import unittest

import numpy as np
from PIL import Image

import app


def make_png(size=32):
    buf = io.BytesIO()
    Image.fromarray(np.zeros((size, size, 3), dtype=np.uint8)).save(buf, "PNG")
    buf.seek(0)
    return buf


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_index_ok(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_reject_missing_file(self):
        r = self.client.post("/predict", data={})
        self.assertEqual(r.status_code, 400)

    def test_reject_bad_type(self):
        r = self.client.post("/predict", data={"file": (io.BytesIO(b"x"), "notes.txt")})
        self.assertEqual(r.status_code, 400)

    def test_reject_too_large(self):
        big = io.BytesIO(b"\0" * (6 * 1024 * 1024))
        r = self.client.post("/predict", data={"file": (big, "big.png")})
        self.assertEqual(r.status_code, 413)

    def test_predict_ok(self):
        r = self.client.post("/predict", data={"file": (make_png(), "img.png")})
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn(data["label"], ("Real", "Fake"))
        self.assertIn("confidence", data)
        self.assertIn("probability", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
