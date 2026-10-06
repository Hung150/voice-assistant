from speech_input import listen
from speech_output import speak
from nlp import parse_command, check_wake_word
from actions import play_music, search_info, get_time, set_alarm
from weather import get_weather_by_name


def ring():
    """Gọi khi đến giờ báo thức."""
    for _ in range(3):
        speak("Đã đến giờ báo thức! Dậy thôi!")


def handle(text):
    """Xử lý một lệnh. Trả về True nếu cần thoát."""
    intent, data = parse_command(text)
    print("Intent:", intent, "| Du lieu:", data)

    if intent == "exit":
        speak("Tạm biệt, hẹn gặp lại!")
        return True
    elif intent == "play_music":
        speak(play_music(data) if data else "Bạn muốn nghe bài gì?")
    elif intent == "set_alarm":
        if data:
            speak(set_alarm(data[0], data[1], ring))
        else:
            speak("Bạn muốn đặt báo thức lúc mấy giờ?")
    elif intent == "search":
        if data:
            speak(f"Đang tìm kiếm về {data}")
            speak(search_info(data))
        else:
            speak("Bạn muốn tìm kiếm về điều gì?")
    elif intent == "get_time":
        speak(get_time())
    elif intent == "weather":
        speak("Đợi tôi một chút")
        speak(get_weather_by_name(data))
    else:
        speak("Xin lỗi, tôi chưa hiểu lệnh này")
    return False


def run(stop_event, on_user=None):
    """Vòng lặp chính. Dừng khi stop_event được set hoặc người dùng nói 'dừng lại'."""
    while not stop_event.is_set():
        text = listen(timeout=3, phrase_time_limit=6)
        if text is None:
            continue
        print("(nghe duoc):", text)

        woke, rest = check_wake_word(text)
        if not woke:
            continue

        if rest:
            command = rest
        else:
            speak("Dạ, tôi nghe đây")
            command = listen(timeout=8, phrase_time_limit=10)
            if command is None:
                speak("Tôi không nghe thấy lệnh nào")
                continue

        print("Ban noi:", command)
        if on_user:
            on_user(command)
        if handle(command):
            break