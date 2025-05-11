from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Thông tin kết nối MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "170705"
MYSQL_HOST = "127.0.0.1"  # Sử dụng 127.0.0.1 thay vì localhost
MYSQL_PORT = "3306"
MYSQL_DB = "btl_csdl"

# Tạo URL kết nối với các tham số bổ sung
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

# Tạo alias DATABASE_URI cho SQLALCHEMY_DATABASE_URL
DATABASE_URI = SQLALCHEMY_DATABASE_URL

# Tạo engine với các tham số bổ sung
engine = create_engine(
    DATABASE_URI,
    pool_pre_ping=True,  # Kiểm tra kết nối trước khi sử dụng
    pool_recycle=3600,   # Tái sử dụng kết nối sau 1 giờ
    echo=True           # Hiển thị SQL queries để debug
)

# Tạo session factory
db_session = scoped_session(sessionmaker(bind=engine))

# Tạo Base class
Base = declarative_base()
Base.query = db_session.query_property()

# Flask configuration
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds
    
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    return db_session

# Export các biến cần thiết
__all__ = ['DATABASE_URI', 'Base', 'engine', 'get_db']
