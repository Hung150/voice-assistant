import os
import re
import unicodedata
from logger import log_command

import joblib


def normalize(s):
    return unicodedata.normalize("NFC", s.lower().strip())


# ---------- Mô hình ML ----------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intent_model.joblib")
CONFIDENCE_THRESHOLD = 0.5

try:
    _model = joblib.load(MODEL_PATH)
    print("(da tai mo hinh intent)")
except Exception as e:
    _model = None
    print("(khong tai duoc mo hinh, dung tu khoa):", e)


def predict_intent(text):
    """Trả về (intent, độ tin cậy). (None, 0) nếu không có mô hình."""
    if _model is None:
        return None, 0.0
    probs = _model.predict_proba([text])[0]
    best = probs.argmax()
    return _model.classes_[best], float(probs[best])


# ---------- Từ khóa (dự phòng và để cắt lấy nội dung) ----------
MUSIC_TRIGGERS = ["mở bài hát", "mở cho tôi bài", "mở bài", "phát bài", "bật bài",
                  "mở nhạc", "phát nhạc", "bật nhạc", "nghe nhạc", "nghe bài",
                  "tôi muốn nghe", "cho tôi nghe", "hát bài"]
SEARCH_TRIGGERS = ["tìm kiếm về", "tìm kiếm", "tra cứu", "cho tôi biết về",
                   "tìm hiểu về", "giới thiệu về", "kể cho tôi nghe về",
                   "cho tôi thông tin về", "tôi muốn biết về", "nói cho tôi về",
                   "là gì", "là ai"]
ALARM_TRIGGERS = ["báo thức", "nhắc tôi", "đánh thức", "gọi tôi dậy"]
TIME_TRIGGERS = ["mấy giờ", "bây giờ là mấy giờ", "giờ hiện tại"]
WEATHER_TRIGGERS = ["thời tiết", "dự báo thời tiết", "trời hôm nay", "có mưa không"]
EXIT_TRIGGERS = ["dừng lại", "tạm biệt", "kết thúc", "exit", "quit"]

# Từ thừa ở đầu/cuối câu cần bỏ khi lấy tên bài hát, từ khóa tìm kiếm
FILLER_WORDS = ["cho tôi", "giúp tôi", "đi", "nhé", "nha", "với", "đi nhé", "lên", "một chút"]

# Các cách Google hay nghe ra từ "trợ lý ơi"
WAKE_WORDS = ["trợ lý ơi", "trợ lý", "trở lý", "chợ lý", "alo trợ lý"]


def _clean_fillers(text):
    text = text.strip()
    changed = True
    while changed:
        changed = False
        for f in sorted(FILLER_WORDS, key=len, reverse=True):
            if text.endswith(" " + f):
                text = text[: -len(f)].strip()
                changed = True
            elif text.startswith(f + " "):
                text = text[len(f):].strip()
                changed = True
    return text


def _strip_triggers(text, triggers):
    """Cắt cụm kích hoạt và từ thừa, phần còn lại là nội dung cần tìm."""
    for t in sorted(triggers, key=len, reverse=True):
        if t in text:
            text = text.replace(t, "", 1)
            break
    return _clean_fillers(text)


# ---------- Trích xuất thông tin (regex) ----------
def extract_alarm_time(text):
    """Lấy giờ từ câu nói. Trả về (giờ, phút) hoặc None."""
    m = re.search(r"(\d{1,2})\s*(?:giờ|h|:)\s*(\d{1,2})?\s*(rưỡi)?", text)
    if not m:
        return None

    hour = int(m.group(1))
    minute = 0
    if m.group(3):
        minute = 30
    elif m.group(2):
        minute = int(m.group(2))

    if any(w in text for w in ["chiều", "tối"]) and hour < 12:
        hour += 12
    elif "sáng" in text and hour == 12:
        hour = 0

    if hour > 23 or minute > 59:
        return None
    return hour, minute


def extract_place(text):
    """Lấy tên địa điểm sau 'ở', 'tại'."""
    m = re.search(r"(?:ở|tại)\s+(.+)", text)
    if m:
        place = m.group(1)
        for w in ["hôm nay", "ngày mai", "bây giờ", "thế nào", "ra sao",
                  "có mưa không", "có mưa", "không"]:
            place = place.replace(w, "")
        return place.strip() or None
    return None


def extract_data(intent, text):
    """Trích thông tin theo từng intent."""
    if intent == "play_music":
        return _strip_triggers(text, MUSIC_TRIGGERS) or None
    if intent == "search":
        return _strip_triggers(text, SEARCH_TRIGGERS) or None
    if intent == "set_alarm":
        return extract_alarm_time(text)
    if intent == "weather":
        return extract_place(text)
    return None


# ---------- Phân tích lệnh ----------
def parse_command_keywords(text):
    """Cách cũ: chỉ dùng từ khóa. Dùng làm dự phòng."""
    if any(t in text for t in WEATHER_TRIGGERS):
        return "weather", extract_place(text)
    if any(t in text for t in ALARM_TRIGGERS):
        return "set_alarm", extract_alarm_time(text)
    if any(t in text for t in TIME_TRIGGERS):
        return "get_time", None
    if any(t in text for t in MUSIC_TRIGGERS):
        return "play_music", extract_data("play_music", text)
    if any(t in text for t in SEARCH_TRIGGERS):
        return "search", extract_data("search", text)
    return "unknown", text


def parse_command(text):
    """Phân tích câu nói. Trả về (intent, dữ liệu)."""
    text = normalize(text)

    # Lệnh thoát luôn kiểm tra bằng từ khóa: đơn giản và đáng tin nhất
    if any(t in text for t in EXIT_TRIGGERS):
        return "exit", None

    intent, conf = predict_intent(text)
    if intent is not None:
        print(f"(ML doan: {intent} - {conf:.0%})")
        log_command(text, intent, conf)

    if intent is None or conf < CONFIDENCE_THRESHOLD:
        # Không chắc: quay về từ khóa
        return parse_command_keywords(text)

    if intent == "unknown":
        return "unknown", text
    if intent == "exit":
        return "exit", None
    return intent, extract_data(intent, text)


def check_wake_word(text):
    """Trả về (True, phần_lệnh_còn_lại) hoặc (False, None)."""
    text = normalize(text)
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        if w in text:
            rest = text.split(w, 1)[1].strip()
            return True, rest
    return False, None