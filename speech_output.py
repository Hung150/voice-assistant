import asyncio
import os
import tempfile

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import edge_tts
import pygame
from gtts import gTTS

pygame.mixer.init()

VOICE = "vi-VN-HoaiMyNeural"   # đổi thành "vi-VN-NamMinhNeural" nếu muốn giọng nam
RATE = "+0%"                    # tốc độ: "+10%" nhanh hơn, "-10%" chậm hơn

on_speak = None   # GUI gán hàm vào đây để nhận câu trợ lý nói


def _make_edge_audio(text, path):
    """Tạo file mp3 bằng edge-tts."""
    async def _run():
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
        await communicate.save(path)
    asyncio.run(_run())


def _make_gtts_audio(text, path):
    """Phương án dự phòng."""
    gTTS(text=text, lang="vi").save(path)


def speak(text):
    """Đọc to văn bản và in ra màn hình."""
    print("Tro ly:", text)
    if on_speak:
        on_speak(text)

    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            path = f.name

        try:
            _make_edge_audio(text, path)
        except Exception as e:
            print("(edge-tts loi, dung gTTS thay the):", e)
            _make_gtts_audio(text, path)

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.unload()
    except Exception as e:
        print("Loi phat giong noi:", e)
    finally:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass