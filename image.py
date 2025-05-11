import os
import mysql.connector

# Kết nối database
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="chip0411",
    database="hotel_management"
)
cursor = conn.cursor()

try:
    hotel_id = 10  # ví dụ ID khách sạn là 10
    base_dir = "hotelsmanagementweb/assets/10"  # đường dẫn tương đối

    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Thư mục không tồn tại: {base_dir}")

    # Lưu ảnh khách sạn chung
    for file in os.listdir(base_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # Tạo đường dẫn tương đối cho database
            image_path = f"/assets/10/{file}"
            cursor.execute("INSERT INTO hotel_images (hotel_id, image_path) VALUES (%s, %s)", (hotel_id, image_path))

    # Lưu ảnh các loại phòng (folder 28, 29, 30)
    for folder_name in ['28', '29', '30']:
        room_id = int(folder_name)
        folder_path = os.path.join(base_dir, folder_name)
        
        # Kiểm tra xem thư mục phòng có tồn tại không
        if not os.path.exists(folder_path):
            print(f"Thư mục phòng {folder_name} không tồn tại")
            continue
            
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                # Tạo đường dẫn tương đối cho database
                image_path = f"/assets/10/{folder_name}/{file}"
                cursor.execute("INSERT INTO room_images (room_id, image_path) VALUES (%s, %s)", (room_id, image_path))

    conn.commit()
    print("Đã lưu toàn bộ ảnh thành công vào database!")

except FileNotFoundError as e:
    print(f"Lỗi: {e}")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
