from config import engine
from sqlalchemy import text

def test_connection():
    try:
        # Thử kết nối với database
        with engine.connect() as connection:
            print("Kết nối MySQL thành công!")
            # Thử thực hiện một truy vấn đơn giản
            result = connection.execute(text("SELECT 1"))
            print("Truy vấn test thành công!")
    except Exception as e:
        print(f"Lỗi kết nối: {str(e)}")

if __name__ == "__main__":
    test_connection() 