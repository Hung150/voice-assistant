import csv
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "command_log.csv")
FIELDS = ["time", "text", "predicted", "confidence", "label"]


def log_command(text, predicted, confidence):
    """Ghi 1 dòng log. Cột 'label' để trống, bạn sẽ điền tay sau."""
    new_file = not os.path.exists(LOG_PATH)
    try:
        # utf-8-sig để Excel mở tiếng Việt không bị lỗi font
        with open(LOG_PATH, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            if new_file:
                w.writerow(FIELDS)
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        text, predicted, f"{confidence:.2f}", ""])
    except OSError as e:
        print("Khong ghi duoc log:", e)