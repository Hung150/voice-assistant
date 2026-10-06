import webbrowser
from urllib.parse import quote_plus

import wikipedia
import threading
import time
from datetime import datetime, timedelta

wikipedia.set_lang("vi")


def play_music(song):
    """Mở kết quả tìm kiếm YouTube cho bài hát/ca sĩ."""
    url = "https://www.youtube.com/results?search_query=" + quote_plus(song)
    webbrowser.open(url)
    return f"Đang mở {song} trên YouTube"


def search_info(query):
    """Tìm trên Wikipedia tiếng Việt, trả về đoạn tóm tắt ngắn (2 câu)."""
    try:
        return wikipedia.summary(query, sentences=2, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        # Từ khóa có nhiều nghĩa: lấy kết quả đầu tiên
        try:
            return wikipedia.summary(e.options[0], sentences=2, auto_suggest=False)
        except Exception:
            return f"Có nhiều kết quả cho {query}, bạn hãy nói cụ thể hơn."
    except wikipedia.exceptions.PageError:
        # Không có trang đúng tên: thử tìm gần đúng
        results = wikipedia.search(query, results=1)
        if results:
            try:
                return wikipedia.summary(results[0], sentences=2, auto_suggest=False)
            except Exception:
                pass
        return f"Tôi không tìm thấy thông tin về {query}."
    except Exception as e:
        print("Loi Wikipedia:", e)
        return "Xin lỗi, tôi không tìm kiếm được lúc này."
    
    
def get_time():
    """Trả về câu nói giờ hiện tại."""
    now = datetime.now()
    return f"Bây giờ là {now.hour} giờ {now.minute} phút"


def _alarm_worker(target, on_ring):
    """Chạy nền: chờ đến giờ rồi gọi on_ring()."""
    while datetime.now() < target:
        time.sleep(1)
    on_ring()


def set_alarm(hour, minute, on_ring):
    """Đặt báo thức lúc hour:minute. Nếu giờ đã qua hôm nay thì đặt cho ngày mai."""
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)

    t = threading.Thread(target=_alarm_worker, args=(target, on_ring), daemon=True)
    t.start()

    ngay = "ngày mai" if target.date() != now.date() else "hôm nay"
    return f"Đã đặt báo thức lúc {hour} giờ {minute} phút {ngay}"