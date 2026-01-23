from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import random
import os
from datetime import datetime

# Khởi tạo ứng dụng
app = FastAPI()

# --- HÀM XỬ LÝ FILE ---
def load_videos():
    """Đọc file videos.txt và lọc bỏ dòng trống"""
    filename = 'videos.txt'
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        # Đọc từng dòng, xóa khoảng trắng thừa
        lines = [line.strip() for line in f.readlines()]
        # Chỉ lấy những dòng có chữ (không rỗng)
        valid_links = [line for line in lines if line]
        
    return valid_links

# Load danh sách video vào bộ nhớ ngay khi chạy server
video_list = load_videos()

# --- CÁC ĐƯỜNG DẪN (ENDPOINTS) ---

@app.get("/")
def home():
    """Trang chủ: Để kiểm tra server có sống không"""
    return {
        "message": "API đang chạy bình thường!",
        "instructions": "Truy cập /videos/gai để lấy JSON, hoặc /watch để xem video."
    }

@app.get("/videos/gai")
def get_girl_video():
    """
    API chính: Trả về JSON thông tin video.
    Dùng @app.get để trình duyệt có thể truy cập được.
    """
    # Lấy ngày giờ hiện tại
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Nếu danh sách trống
    if not video_list:
        return {
            "status": False,
            "data": None,
            "count": 0,
            "update_time": current_date
        }
    
    # Lấy ngẫu nhiên
    url = random.choice(video_list)
    
    # Trả về đúng định dạng bạn yêu cầu
    return {
        "status": True,
        "data": url,
        "count": len(video_list),
        "update_time": current_date
    }

@app.get("/watch")
def watch_random_video():
    """
    API phụ: Tự động chuyển hướng (Redirect) sang trang xem video.
    """
    if not video_list:
        return {"error": "Danh sách video trống!"}
        
    url = random.choice(video_list)
    return RedirectResponse(url)

# Dòng này để chạy dưới máy local (nếu cần)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
