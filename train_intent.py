import csv
import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from intent_data import build_dataset

LOG_PATH = "command_log.csv"
VALID = {"play_music", "search", "set_alarm", "get_time", "weather", "exit", "unknown"}
REAL_WEIGHT = 5   # câu thật được lặp 5 lần để mô hình coi trọng hơn câu sinh tự động


def load_real_data():
    """Đọc các dòng đã gán nhãn trong log."""
    X, y = [], []
    if not os.path.exists(LOG_PATH):
        return X, y
    with open(LOG_PATH, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            label = (row.get("label") or "").strip()
            text = (row.get("text") or "").strip().lower()
            if text and label in VALID:
                X += [text] * REAL_WEIGHT
                y += [label] * REAL_WEIGHT
    return X, y


def make_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True)),
        ("clf", LogisticRegression(max_iter=1000, C=10)),
    ])


X, y = build_dataset()
real_X, real_y = load_real_data()
print(f"Cau sinh tu dong: {len(X)} | Cau that (da nhan, x{REAL_WEIGHT}): {len(real_X)}")
X += real_X
y += real_y

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
model = make_pipeline()
model.fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te), zero_division=0))

final = make_pipeline()
final.fit(X, y)
joblib.dump(final, "intent_model.joblib")
print("Da luu mo hinh: intent_model.joblib")