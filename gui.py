import queue
import threading
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext

import speech_input
import speech_output
from assistant import run

STATUS = {
    "idle":       ("Đang nghỉ",         "#888888"),
    "listening":  ("Đang nghe...",      "#2e9e4f"),
    "processing": ("Đang xử lý...",     "#e08a00"),
    "speaking":   ("Đang nói...",       "#1f6feb"),
}


class App:
    def __init__(self, root):
        self.root = root
        root.title("Trợ lý ảo")
        root.geometry("480x560")

        self.q = queue.Queue()        # thông điệp từ luồng nền sang giao diện
        self.stop_event = None
        self.thread = None

        # Nhãn trạng thái
        self.status = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), pady=10)
        self.status.pack(fill="x")

        # Khung hội thoại
        self.chat = scrolledtext.ScrolledText(
            root, state="disabled", wrap="word", font=("Segoe UI", 11), padx=8, pady=8
        )
        self.chat.pack(fill="both", expand=True, padx=10)
        self.chat.tag_config("user", foreground="#1f6feb", justify="right")
        self.chat.tag_config("bot", foreground="#222222")
        self.chat.tag_config("sys", foreground="#888888", justify="center")

        # Nút bấm
        self.btn = tk.Button(
            root, text="Bắt đầu", font=("Segoe UI", 12, "bold"),
            command=self.toggle, height=2
        )
        self.btn.pack(fill="x", padx=10, pady=10)

        self.set_status("idle")
        self.add_message("sys", "Bấm 'Bắt đầu', rồi nói: \"trợ lý ơi ...\"")

        # Nhận trạng thái và lời nói từ luồng nền (chỉ đưa vào queue)
        speech_input.on_status = lambda s: self.q.put(("status", s))
        speech_output.on_speak = lambda t: self.q.put(("bot", t))

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.poll()

    # ----- cập nhật giao diện (chỉ gọi từ luồng chính) -----
    def set_status(self, key):
        text, color = STATUS[key]
        self.status.config(text=text, fg=color)

    def add_message(self, kind, text):
        prefix = {"user": "Bạn", "bot": "Trợ lý", "sys": ""}[kind]
        stamp = datetime.now().strftime("%H:%M")
        line = f"[{stamp}] {prefix}: {text}\n\n" if prefix else f"{text}\n\n"
        self.chat.config(state="normal")
        self.chat.insert("end", line, kind)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def poll(self):
        """Mỗi 100ms lấy thông điệp từ queue và cập nhật giao diện."""
        try:
            while True:
                msg = self.q.get_nowait()
                kind = msg[0]
                if kind == "status":
                    self.set_status(msg[1])
                elif kind == "bot":
                    self.set_status("speaking")
                    self.add_message("bot", msg[1])
                elif kind == "user":
                    self.add_message("user", msg[1])
                elif kind == "finished":
                    self.on_finished()
        except queue.Empty:
            pass
        self.root.after(100, self.poll)

    # ----- điều khiển -----
    def toggle(self):
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.btn.config(text="Đang dừng...", state="disabled")
        else:
            self.start()

    def start(self):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.worker, daemon=True)
        self.thread.start()
        self.btn.config(text="Dừng")
        self.add_message("sys", "Trợ lý đã bắt đầu. Hãy nói \"trợ lý ơi\".")

    def worker(self):
        """Chạy ở luồng nền."""
        try:
            run(self.stop_event, on_user=lambda t: self.q.put(("user", t)))
        except Exception as e:
            print("Loi:", e)
        finally:
            self.q.put(("finished",))

    def on_finished(self):
        self.set_status("idle")
        self.btn.config(text="Bắt đầu", state="normal")
        self.add_message("sys", "Trợ lý đã dừng.")

    def on_close(self):
        if self.stop_event:
            self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()