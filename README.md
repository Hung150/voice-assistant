# Trợ lý ảo tiếng Việt (Voice Assistant)

Trợ lý ảo điều khiển bằng giọng nói tiếng Việt, viết bằng Python. Trợ lý nghe lệnh qua micro, hiểu ý định bằng mô hình học máy, thực thi tác vụ và trả lời bằng giọng nói. Có giao diện Tkinter.

## Tính năng

| Lệnh | Ví dụ câu nói | Cách hoạt động |
|---|---|---|
| Phát nhạc | "trợ lý ơi mở nhạc sơn tùng" | Mở kết quả tìm kiếm YouTube |
| Tìm kiếm thông tin | "trợ lý ơi tìm kiếm về hà nội" | Đọc tóm tắt từ Wikipedia tiếng Việt |
| Báo thức | "trợ lý ơi đặt báo thức lúc 7 giờ rưỡi" | Luồng nền canh giờ, đến giờ thì đọc thông báo |
| Xem giờ | "trợ lý ơi mấy giờ rồi" | Đọc giờ hệ thống |
| Thời tiết | "trợ lý ơi thời tiết ở đà nẵng" | Gọi API Open-Meteo (không cần key) |
| Thoát | "trợ lý ơi dừng lại" | Tắt trợ lý |

Trợ lý chỉ phản hồi khi nghe từ đánh thức **"trợ lý ơi"**. Có thể nói liền cả câu, hoặc gọi trước, chờ trợ lý đáp "Dạ, tôi nghe đây" rồi mới nói lệnh.

## Kiến trúc

```
Micro -> Google Speech Recognition -> Wake word
      -> Mô hình ML đoán intent (TF-IDF + Logistic Regression)
         (từ khóa làm dự phòng khi độ tin cậy thấp)
      -> Regex trích thông tin (giờ, tên bài hát, địa điểm)
      -> Thực thi (YouTube / Wikipedia / Open-Meteo / datetime)
      -> edge-tts phát giọng nói -> Giao diện Tkinter
      -> Ghi log câu nói thật -> Gán nhãn -> Huấn luyện lại
```

## Cấu trúc thư mục

```
voice-assistant/
├── gui.py               # Giao diện Tkinter (chạy file này)
├── main.py              # Bản chạy trên terminal
├── assistant.py         # Vòng lặp chính và xử lý lệnh (dùng chung)
├── speech_input.py      # Nghe micro, nhận dạng giọng nói
├── speech_output.py     # Phát giọng nói (edge-tts, dự phòng gTTS)
├── nlp.py               # Wake word, intent, trích xuất thông tin
├── actions.py           # Nhạc, tìm kiếm, giờ, báo thức
├── weather.py           # Thời tiết (Open-Meteo)
├── logger.py            # Ghi log câu nói vào command_log.csv
├── intent_data.py       # Dữ liệu huấn luyện sinh từ mẫu câu
├── train_intent.py      # Huấn luyện mô hình intent
├── intent_model.joblib  # Mô hình đã huấn luyện
├── requirements.txt     # Danh sách thư viện
└── README.md
```

`command_log.csv` được tạo tự động khi dùng trợ lý (không đưa lên Git).

## Cài đặt

Yêu cầu: Python 3.9+, micro, loa hoặc tai nghe, kết nối internet.

```bash
# 1. Tải dự án
git clone https://github.com/Hung150/voice-assistant.git
cd voice-assistant

# 2. Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\activate          # Windows (cmd)
# source venv/bin/activate     # macOS / Linux

# 3. Cài thư viện
pip install -r requirements.txt
```

Mô hình `intent_model.joblib` đã có sẵn. Nếu muốn huấn luyện lại, chạy `python train_intent.py`.

**Lỗi cài PyAudio trên Windows:** thử `pip install pipwin` rồi `pipwin install pyaudio`.

## Cách chạy

```bash
python gui.py     # giao diện: bấm "Bắt đầu" rồi nói "trợ lý ơi ..."
python main.py    # bản terminal
```

Nên **đeo tai nghe** khi dùng để micro không thu lại giọng của trợ lý.

## Cải thiện mô hình bằng câu nói thật

1. Dùng trợ lý bình thường, mỗi lệnh được ghi vào `command_log.csv`.
2. Mở file bằng Excel, điền cột `label` bằng intent đúng: `play_music`, `search`, `set_alarm`, `get_time`, `weather`, `exit`, `unknown`.
3. Chạy lại `python train_intent.py`. Mô hình sẽ học thêm từ các câu đã gán nhãn.

Nếu một câu bị hiểu sai, có thể thêm mẫu câu tương tự vào `intent_data.py` rồi huấn luyện lại.

## Tùy chỉnh

- **Giọng nói:** sửa `VOICE` trong `speech_output.py` (`vi-VN-HoaiMyNeural` nữ, `vi-VN-NamMinhNeural` nam).
- **Địa điểm thời tiết mặc định:** sửa `DEFAULT_PLACE` trong `weather.py`.
- **Từ đánh thức:** sửa `WAKE_WORDS` trong `nlp.py`.
- **Ngưỡng tin cậy của mô hình:** sửa `CONFIDENCE_THRESHOLD` trong `nlp.py`.

## Hạn chế

- Nhận dạng giọng nói và giọng đọc cần internet; Google Speech đôi khi nhận sai chữ.
- Báo thức chỉ tồn tại khi chương trình đang chạy.
- Mô hình intent nhỏ, huấn luyện chủ yếu từ dữ liệu sinh tự động nên cần bổ sung câu nói thật để chính xác hơn.
- Lệnh nhạc chỉ mở trang tìm kiếm YouTube, chưa tự phát video.

## Công nghệ

SpeechRecognition, edge-tts, gTTS, pygame, scikit-learn, Wikipedia API, Open-Meteo API, Tkinter.