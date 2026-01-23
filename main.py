from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import random
import os
from datetime import datetime

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

def load_videos():
    """
    Hàm này đọc file videos.txt và trả về danh sách các đường link.
    Nó tự động loại bỏ các dòng trống hoặc khoảng trắng thừa.
    """
    filename = 'videos.txt'
    
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(filename):
        print(f"Lỗi: Không tìm thấy file {filename}")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        # Đọc từng dòng, dùng strip() để xóa xuống dòng và khoảng trắng
        lines = [line.strip() for line in f.readlines()]
        
        # Chỉ giữ lại những dòng có nội dung (không rỗng)
        valid_links = [line for line in lines if line]
        
    return valid_links

# Load danh sách video vào biến toàn cục ngay khi server khởi động
video_list = load_videos()

@app.get("/")
def home():
    """
    Trang chủ giới thiệu API
    """
    return {
        "message": "Welcome to Video API",
        "endpoint": "/videos/gai",
        "total_videos": len(video_list),
        "status": "Running"
    }

@app.get("/videos/gai")
def get_girl_video():
    """
    API trả về link video ngẫu nhiên theo định dạng JSON yêu cầu.
    Endpoint: /videos/gai
    """
    # Lấy ngày hiện tại format Ngày/Tháng/Năm (ví dụ: 23/01/2026)
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Trường hợp 1: Danh sách video bị rỗng hoặc lỗi file
    if not video_list:
        return {
            "status": False,
            "data": None,
            "count": 0,
            "update_time": current_date
        }
    
    # Trường hợp 2: Có video, lấy ngẫu nhiên 1 video
    random_video_url = random.choice(video_list)
    
    return {
        "status": True,
        "data": random_video_url,
        "count": len(video_list),
        "update_time": current_date
    }

@app.get("/watch")
def watch_random_video():
    """
    API phụ: Chuyển hướng người dùng đến xem trực tiếp video
    thay vì trả về JSON.
    """
    if not video_list:
        return {"error": "Danh sách video trống, vui lòng kiểm tra file videos.txt"}
        
    random_video_url = random.choice(video_list)
    return RedirectResponse(random_video_url)

# Đoạn code này giúp bạn có thể chạy thử trên máy tính cá nhân
# bằng lệnh: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
