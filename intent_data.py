import random

random.seed(42)

SONGS = ["sơn tùng", "em của ngày hôm qua", "đen vâu", "hà anh tuấn", "mỹ tâm",
         "lạc trôi", "nơi này có anh", "bích phương", "nhạc trẻ", "nhạc lofi",
         "nhạc không lời", "hoàng thùy linh", "chúng ta của hiện tại"]
TOPICS = ["hà nội", "python", "việt nam", "trí tuệ nhân tạo", "núi phú sĩ",
          "đại học bách khoa", "hồ chí minh", "cà phê", "bóng đá", "vũ trụ",
          "hồ gươm", "internet", "chủ tịch hồ chí minh"]
TIMES = ["7 giờ", "6 giờ 30", "5h sáng", "7 giờ rưỡi tối", "8 giờ 15", "6h30",
         "9 giờ tối", "5 giờ chiều", "10 giờ 45", "4 giờ sáng"]
PLACES = ["hà nội", "đà nẵng", "hồ chí minh", "huế", "bắc giang", "hải phòng", "đà lạt"]

TEMPLATES = {
    "play_music": [
        "mở nhạc {s}", "phát bài {s}", "bật bài {s} cho tôi", "tôi muốn nghe {s}",
        "cho tôi nghe {s}", "nghe nhạc {s} đi", "mở bài hát {s}", "bật nhạc {s}",
        "phát nhạc {s} nhé", "mở cho tôi bài {s}", "hát bài {s} đi",
        "bật nhạc lên", "mở nhạc đi", "phát nhạc giúp tôi", "tôi muốn nghe nhạc",
    ],
    "search": [
        "tìm kiếm về {t}", "tìm kiếm {t}", "{t} là gì", "tra cứu {t}",
        "cho tôi biết về {t}", "tìm hiểu về {t}", "giới thiệu về {t}",
        "{t} là ai", "kể cho tôi nghe về {t}", "cho tôi thông tin về {t}",
        "tôi muốn biết về {t}", "nói cho tôi về {t}",
    ],
    "set_alarm": [
        "đặt báo thức lúc {h}", "báo thức {h}", "hẹn giờ báo thức {h}",
        "đánh thức tôi lúc {h}", "nhắc tôi dậy lúc {h}", "đặt chuông báo thức {h}",
        "cài báo thức lúc {h}", "đặt cho tôi báo thức {h}", "gọi tôi dậy lúc {h}",
        "đặt báo thức", "hẹn giờ đánh thức tôi",
    ],
    "get_time": [
        "mấy giờ rồi", "bây giờ là mấy giờ", "cho tôi biết giờ", "giờ hiện tại là mấy giờ",
        "bây giờ mấy giờ rồi", "xem giờ giúp tôi", "đồng hồ chỉ mấy giờ",
        "hiện tại là mấy giờ", "nói cho tôi giờ hiện tại", "giờ giấc bây giờ thế nào",
    ],
    "weather": [
        "thời tiết hôm nay", "thời tiết ở {p}", "dự báo thời tiết tại {p}",
        "hôm nay trời thế nào", "trời hôm nay có mưa không", "ở {p} có mưa không",
        "nhiệt độ hôm nay bao nhiêu", "hôm nay nóng không", "trời {p} hôm nay ra sao",
        "thời tiết {p} thế nào", "ngày mai có mưa không", "hôm nay có cần mang ô không",
        "trời có lạnh không", "dự báo thời tiết", "hôm nay có nóng không", "hôm nay có lạnh không", "trời hôm nay có nóng không",
        "hôm nay trời có nóng không", "ngoài trời nóng không", "bây giờ trời nóng không",
        "hôm nay nhiệt độ bao nhiêu độ", "hôm nay có nắng không", "trời có nắng không",
        "ngày mai có nóng không", "ở {p} hôm nay có nóng không", "hôm nay ở {p} lạnh không",
    ],
    "exit": [
        "dừng lại", "tạm biệt", "kết thúc", "thoát đi", "tắt đi", "dừng chương trình",
        "tạm biệt nhé", "hẹn gặp lại", "thôi không cần nữa", "kết thúc chương trình",
        "tôi đi đây tạm biệt", "tắt trợ lý đi",
    ],
    # Câu không thuộc lệnh nào: giúp mô hình biết "từ chối"
    "unknown": [
        "hôm nay trời đẹp quá", "tôi đói bụng rồi", "bạn khỏe không", "cảm ơn nhé",
        "ăn cơm chưa", "tôi buồn ngủ quá", "ôi mệt quá", "chào buổi sáng",
        "hôm nay đi học vui lắm", "không có gì đâu", "ừ được rồi", "để tôi nghĩ đã",
        "cái này hay đấy", "tối nay ăn gì nhỉ", "bạn tên là gì", "tôi chán quá",
        "ngày mai đi chơi nhé", "đúng rồi", "không biết nữa", "lát nữa nói chuyện sau",
    ],
}


def build_dataset(per_template=6):
    """Trả về (danh sách câu, danh sách nhãn)."""
    X, y = [], []
    for intent, templates in TEMPLATES.items():
        for tpl in templates:
            if "{" not in tpl:
                X.extend([tpl] * per_template)
                y.extend([intent] * per_template)
                continue
            for _ in range(per_template):
                X.append(tpl.format(
                    s=random.choice(SONGS), t=random.choice(TOPICS),
                    h=random.choice(TIMES), p=random.choice(PLACES),
                ))
                y.append(intent)
    return X, y