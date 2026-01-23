from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import random
import os
from datetime import datetime

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

def load_videos():
    """
    Hàm đọc file videos.txt.
    LƯU Ý QUAN TRỌNG CHO VERCEL:
    Trên Vercel, chúng ta phải dùng đường dẫn tuyệt đối (os.path.abspath)
    để tìm thấy file txt nằm cùng thư mục với file code.
    """
    try:
        # Lấy đường dẫn của thư mục hiện tại chứa file main.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ghép thành đường dẫn đầy đủ tới file videos.txt
        file_path = os.path.join(current_dir, 'videos.txt')
        
        # Kiểm tra xem file có tồn tại không
        if not os.path.exists(file_path):
            print(f"Lỗi: Không tìm thấy file tại {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # Đọc từng dòng và xóa khoảng trắng thừa
            lines = [line.strip() for line in f.readlines()]
            # Chỉ lấy những dòng có nội dung (không rỗng)
            valid_links = [line for line in lines if line]
            
        return valid_links
        
    except Exception as e:
        print(f"Có lỗi khi đọc file: {str(e)}")
        return []

# Load danh sách video vào biến toàn cục
# Lưu ý: Trên Vercel, biến này sẽ được load lại mỗi khi function được gọi (cold start)
video_list = load_videos()

@app.get("/")
def home():
    """
    Trang chủ giới thiệu API
    """
    return {
        "message": "API Video đang chạy trên Vercel!",
        "endpoint": "/videos/gai",
        "instructions": "Thêm /videos/gai vào cuối đường dẫn để lấy JSON."
    }

@app.get("/videos/gai")
def get_girl_video():
    """
    API trả về link video ngẫu nhiên theo định dạng JSON yêu cầu.
    """
    # Nếu vì lý do nào đó danh sách chưa được load, load lại lần nữa
    global video_list
    if not video_list:
        video_list = load_videos()

    # Lấy ngày hiện tại format Ngày/Tháng/Năm
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Trường hợp danh sách video vẫn rỗng
    if not video_list:
        return {
            "status": False,
            "data": None,
            "count": 0,
            "update_time": current_date,
            "error": "Không tìm thấy video nào"
        }
    
    # Lấy ngẫu nhiên 1 video
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
    Chuyển hướng người dùng đến xem trực tiếp video
    """
    # Load lại danh sách nếu rỗng
    global video_list
    if not video_list:
        video_list = load_videos()

    if not video_list:
        return {"error": "Danh sách video trống!"}
        
    random_video_url = random.choice(video_list)
    return RedirectResponse(random_video_url)
