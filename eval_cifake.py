import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
from datasets import load_dataset
from tensorflow.keras.models import load_model

from config import IMG_HEIGHT, IMG_WIDTH, MODEL_PATH, RESCALE

DATASET_ID = "dragonintelligence/CIFAKE-image-dataset"
BATCH_SIZE = 256


def compute_metrics(y_true, y_score, threshold=0.5):
    y_pred = (y_score >= threshold).astype(int)

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    accuracy = (tp + tn) / max(1, len(y_true))
    precision_real = tp / max(1, tp + fp)
    recall_real = tp / max(1, tp + fn)
    f1_real = 2 * precision_real * recall_real / max(1e-9, precision_real + recall_real)

    precision_fake = tn / max(1, tn + fn)
    recall_fake = tn / max(1, tn + fp)
    f1_fake = 2 * precision_fake * recall_fake / max(1e-9, precision_fake + recall_fake)

    precision_macro = (precision_real + precision_fake) / 2
    recall_macro = (recall_real + recall_fake) / 2
    f1_macro = (f1_real + f1_fake) / 2

    order = np.argsort(y_score)
    s = y_score[order]
    y = y_true[order]
    pos = int(np.sum(y == 1))
    neg = len(y) - pos
    auc = float("nan")
    if pos > 0 and neg > 0:
        ranks = np.empty(len(y), dtype=np.float64)
        i = 0
        while i < len(y):
            j = i
            while j + 1 < len(y) and s[j + 1] == s[i]:
                j += 1
            ranks[i : j + 1] = (i + j) / 2.0 + 1.0
            i = j + 1
        auc = float((ranks[y == 1].sum() - pos * (pos + 1) / 2.0) / (pos * neg))

    return {
        "accuracy": accuracy,
        "confusion_matrix": np.array([[tn, fp], [fn, tp]]),
        "real": {"precision": precision_real, "recall": recall_real, "f1": f1_real},
        "fake": {"precision": precision_fake, "recall": recall_fake, "f1": f1_fake},
        "macro": {"precision": precision_macro, "recall": recall_macro, "f1": f1_macro},
        "roc_auc": auc,
    }


def main():
    print("Loading model...")
    model = load_model(MODEL_PATH)
    print("Loading CIFAKE test split...")
    ds = load_dataset(DATASET_ID, split="test")

    y_true = np.asarray(ds["label"], dtype=int)
    n = len(y_true)
    n_real = int(np.sum(y_true == 1))
    n_fake = n - n_real
    print(f"Test samples: {n} ({n_real} Real, {n_fake} Fake)")

    probs = np.zeros(n, dtype=np.float32)
    for i in range(0, n, BATCH_SIZE):
        batch = ds[i : i + BATCH_SIZE]["image"]
        arrs = np.stack([np.asarray(img.convert("RGB"), dtype=np.float32) for img in batch])
        if RESCALE:
            arrs /= 255.0
        preds = model.predict(arrs, verbose=0, batch_size=BATCH_SIZE)
        probs[i : i + len(batch)] = preds[:, 0]

    metrics = compute_metrics(y_true, probs)
    cm = metrics["confusion_matrix"]

    print("\n" + "=" * 50)
    print("CIFAKE EVALUATION - my_model21.h5")
    print("=" * 50)
    print(f"Test samples : {n} (Real={n_real}, Fake={n_fake})")
    print(f"Accuracy     : {metrics['accuracy']:.4f}  ({metrics['accuracy']*100:.2f}%)")
    print(f"ROC-AUC      : {metrics['roc_auc']:.4f}")
    print()
    print("Confusion matrix (rows=actual, cols=predicted):")
    print("                 Pred Fake   Pred Real")
    print(f"  Actual Fake     {cm[0,0]:6d}      {cm[0,1]:6d}")
    print(f"  Actual Real     {cm[1,0]:6d}      {cm[1,1]:6d}")
    print()
    print(f"{'Class':<8}{'Precision':>12}{'Recall':>10}{'F1':>10}")
    for name in ("real", "fake", "macro"):
        m = metrics[name]
        print(f"{name.capitalize():<8}{m['precision']:>12.4f}{m['recall']:>10.4f}{m['f1']:>10.4f}")


if __name__ == "__main__":
    main()
