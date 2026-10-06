import threading
from assistant import run

print("Tro ly dang cho. Hay noi 'tro ly oi' de danh thuc.")
try:
    run(threading.Event())
except KeyboardInterrupt:
    print("\nDa dung chuong trinh.")