# AGENTS.md

## Environment (critical)
- System `python` is 3.14; TensorFlow has **no wheels for 3.14**. Always use the venv:
  `.\.venv\Scripts\python.exe` (Python 3.12.10). Never `python`/`pip` directly.
- Recreate venv: `py -3.12 -m venv .venv` then `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
- TensorFlow runs CPU-only on native Windows.
- No `.gitignore` until first commit; do not commit `.venv/` or `__pycache__/`.

## Run the app
- Start: `.\.venv\Scripts\python.exe app.py` -> http://127.0.0.1:5000
- `GET /` = UI; `POST /predict` = multipart field `file` -> JSON `{label, probability, confidence}`.
- No tests/lint/typecheck. Syntax check: `.\.venv\Scripts\python.exe -m py_compile app.py eval_cifake.py`

## Model & preprocessing
- `model/my_model21.h5` = Keras CNN, input 32x32x3 RGB, single sigmoid output (0=Fake, 1=Real).
- Preprocessing must match `app.py`: RGB -> resize (32,32) LANCZOS -> divide by 255.
- Class mapping: sigmoid >= 0.5 -> `CLASS_1` ("Real"), else `CLASS_0` ("Fake").
- `IMG_WIDTH/HEIGHT`, `RESCALE`, `CLASS_0/1`, `MODEL_PATH` live in `config.py` — shared by `app.py` and `eval_cifake.py`.

## Evaluation
- `.\.venv\Scripts\python.exe eval_cifake.py` — on first run downloads the CIFAKE test split
  (~8 MB parquet, 20k imgs) from Hugging Face into `~/.cache/huggingface`; needs network.
- Reference baseline: accuracy 93.95%, ROC-AUC 0.9861.

## UI
- Interface text is Indonesian; result badge stays English REAL/FAKE. Keep class labels untranslated.
