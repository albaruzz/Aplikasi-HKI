# AGENTS.md

## Environment (critical)
- System `python3` is 3.14; TensorFlow has **no wheels for 3.14**. Always use the venv:
  `.venv/bin/python` (Python 3.12). Never run `python3`/`pip` directly.
- The `.venv` was created by `uv` and has **no `pip` module** — do not use `.venv/bin/python -m pip`.
  To reinstall deps: `uv pip install -r requirements.txt` (uv is at `~/.local/bin/uv`).
  To recreate: `python3.12 -m venv .venv` then `.venv/bin/python -m pip install -r requirements.txt`.
- TensorFlow runs CPU-only (no CUDA). CUDA/cuInit warnings on stderr are harmless; expect them.
- There is a stray 3.14 venv at `venv/` — ignore it; always use `.venv/`.
- `.gitignore` excludes `.venv/`, `__pycache__/`, `*.pyc`; `.gitattributes` pins LF + marks `*.h5` binary.

## Run the app
- Start: `.venv/bin/python app.py` -> http://127.0.0.1:5000
- `GET /` = UI; `POST /predict` = multipart field `file` -> JSON `{label, probability, confidence}`.
- Smoke tests: `.venv/bin/python smoke_test.py` (stdlib unittest; loads TF, ~seconds).
- No lint/typecheck. Syntax check: `.venv/bin/python -m py_compile app.py eval_cifake.py smoke_test.py`

## Model & preprocessing
- `model/my_model21.h5` = Keras CNN, input 32x32x3 RGB, single sigmoid output (0=Fake, 1=Real).
- Preprocessing must match `app.py`: RGB -> resize (32,32) LANCZOS -> divide by 255.
- Class mapping: sigmoid >= 0.5 -> `CLASS_1` ("Real"), else `CLASS_0` ("Fake").
- `IMG_WIDTH/HEIGHT`, `RESCALE`, `CLASS_0/1`, `MODEL_PATH` live in `config.py` — shared by `app.py` and `eval_cifake.py`.

## Evaluation
- `.venv/bin/python eval_cifake.py` — on first run downloads the CIFAKE test split
  (~8 MB parquet, 20k imgs) from Hugging Face into `~/.cache/huggingface`; needs network.
- Reference baseline: accuracy 93.95%, ROC-AUC 0.9861.

## UI
- Interface text is Indonesian; result badge stays English REAL/FAKE. Keep class labels untranslated.
