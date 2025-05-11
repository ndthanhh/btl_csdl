import json
import mysql.connector

# Kết nối MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="170705",
    database="dthanh01"
)
cursor = conn.cursor()

# Đọc file JSON
with open("D:\\Newfolder\\myproject\\hotelsmanagementweb\\database\\db.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Chèn dữ liệu vào MySQL
for hotel in data["hotels"]:
    cursor.execute(
        "INSERT INTO hotels (hotel_name, address_hotel, rating) VALUES (%s, %s, %s)",
        (hotel["hotel_name"], hotel["address_hotel"], hotel["rating"])
    )
    hotel_id = cursor.lastrowid  # Lấy ID khách sạn vừa thêm

    for room in hotel["rooms"]:
        cursor.execute(
            "INSERT INTO rooms (hotel_id, room_number, type, price_per_night) VALUES (%s, %s, %s, %s)",
            (hotel_id, room["room_number"], room["type"], room["price_per_night"])
        )
        room_id = cursor.lastrowid  # Lấy ID phòng vừa thêm

        for service in room["services"]:
            cursor.execute(
                "INSERT INTO services (room_id, service_name) VALUES (%s, %s)",
                (room_id, service)
            )

# Commit và đóng kết nối
conn.commit()
cursor.close()
conn.close()
print("Data imported successfully!")
