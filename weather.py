import requests

# Tọa độ mặc định: Bắc Giang
DEFAULT_PLACE = {"name": "Bắc Giang", "lat": 21.27, "lon": 106.19}

# Mã thời tiết của Open-Meteo -> mô tả tiếng Việt
WEATHER_CODES = {
    0: "trời quang",
    1: "trời gần như quang", 2: "có mây rải rác", 3: "trời nhiều mây",
    45: "có sương mù", 48: "có sương mù",
    51: "mưa phùn nhẹ", 53: "mưa phùn", 55: "mưa phùn dày",
    56: "mưa phùn lạnh", 57: "mưa phùn lạnh",
    61: "mưa nhỏ", 63: "mưa vừa", 65: "mưa to",
    66: "mưa lạnh", 67: "mưa lạnh",
    71: "tuyết nhẹ", 73: "tuyết", 75: "tuyết dày", 77: "hạt tuyết",
    80: "mưa rào nhẹ", 81: "mưa rào", 82: "mưa rào lớn",
    85: "mưa tuyết nhẹ", 86: "mưa tuyết lớn",
    95: "có dông", 96: "có dông kèm mưa đá", 99: "có dông kèm mưa đá lớn",
}


def fetch_weather(lat, lon):
    """Gọi API, trả về dict dữ liệu thô. Trả về None nếu lỗi."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "Asia/Bangkok",
        "forecast_days": 1,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print("Loi goi API thoi tiet:", e)
        return None


def describe_weather(data, place_name):
    """Biến dữ liệu thô thành câu nói tiếng Việt."""
    cur = data["current"]
    day = data["daily"]

    desc = WEATHER_CODES.get(cur["weather_code"], "không rõ")
    temp = round(cur["temperature_2m"])
    humidity = round(cur["relative_humidity_2m"])
    t_max = round(day["temperature_2m_max"][0])
    t_min = round(day["temperature_2m_min"][0])
    rain = day["precipitation_probability_max"][0]

    text = (
        f"Thời tiết {place_name} hiện tại {desc}, {temp} độ C, độ ẩm {humidity} phần trăm. "
        f"Hôm nay thấp nhất {t_min} độ, cao nhất {t_max} độ."
    )
    if rain is not None:
        text += f" Khả năng có mưa là {rain} phần trăm."
    return text


def get_weather(place=DEFAULT_PLACE):
    """Hàm chính: trả về câu mô tả thời tiết."""
    data = fetch_weather(place["lat"], place["lon"])
    if data is None:
        return "Xin lỗi, tôi không lấy được thông tin thời tiết lúc này."
    return describe_weather(data, place["name"])

def find_place(name):
    """Tìm tọa độ theo tên địa điểm. Trả về dict hoặc None."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 1, "language": "vi"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        results = r.json().get("results")
        if not results:
            return None
        p = results[0]
        return {"name": p["name"], "lat": p["latitude"], "lon": p["longitude"]}
    except requests.RequestException as e:
        print("Loi tim dia diem:", e)
        return None


def get_weather_by_name(name=None):
    """Nếu không có tên: dùng Bắc Giang. Có tên: tìm tọa độ rồi lấy thời tiết."""
    if not name:
        return get_weather()
    place = find_place(name)
    if place is None:
        return f"Tôi không tìm thấy địa điểm {name}."
    return get_weather(place)