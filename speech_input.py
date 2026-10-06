import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

on_status = None   # GUI gán hàm vào đây để nhận trạng thái
_calibrated = False


def _status(s):
    if on_status:
        on_status(s)


def listen(timeout=5, phrase_time_limit=8):
    """Nghe từ micro và trả về văn bản (chữ thường), hoặc None."""
    global _calibrated
    with sr.Microphone() as source:
        if not _calibrated:
            print("Dang do tieng on nen, hay giu yen lang...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            _calibrated = True
        print("Dang nghe...")
        _status("listening")
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return None

    _status("processing")
    try:
        return recognizer.recognize_google(audio, language="vi-VN").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Loi ket noi dich vu nhan dang:", e)
        return None