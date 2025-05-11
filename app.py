from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
import flask
from config import engine, Base, get_db
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from functools import wraps
from datetime import datetime, timedelta
from models import User, Hotel, Room, Service, Review, Booking, Payment, UserRole, RoomImage, UserSecurity
from utils import (
    create_user, verify_user, get_available_rooms, create_booking, 
    create_payment, create_review, get_hotel_by_id, get_room_by_id, 
    get_user_by_id, get_booking_by_id, get_user_bookings, get_hotel_reviews,
    send_verification_email, send_password_reset_email
)
import re
from sqlalchemy import text, inspect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from sqlalchemy.sql import func
import locale
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from contextlib import contextmanager
import secrets
from flask_mail import Mail
import hmac, hashlib, urllib.parse

app = Flask(__name__, 
    template_folder='hotelsmanagementweb/pages',
    static_folder='hotelsmanagementweb',
    static_url_path=''
)
app.secret_key = 'your-secret-key'  # Thay thế bằng secret key của bạn
app.permanent_session_lifetime = timedelta(days=7)  # Thời gian lưu session
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_NAME'] = 'hanoibooking_session'  # Tên cookie session
app.config['REMEMBER_COOKIE_NAME'] = 'hanoibooking_remember'  # Tên cookie remember me
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  # Thời gian lưu remember me
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

# Cấu hình Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Thay thế bằng email của bạn
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Thay thế bằng mật khẩu ứng dụng Gmail
mail = Mail(app)

# Set locale cho định dạng số
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

# Custom filter để format số
@app.template_filter('format_number')
def format_number(value):
    try:
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value

# Custom filter để format số tiền
@app.template_filter('format_price')
def format_price(value):
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "0"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Session setup for SQLAlchemy
engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine
db_session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()

@app.errorhandler(Exception)
def handle_error(e):
    db_session.rollback()
    app.logger.error(f"Unhandled error: {str(e)}")
    return "An error occurred. Please try again.", 500

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    if response.status_code >= 400:
        db_session.rollback()
    return response

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này!'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    try:
        return db_session.query(User).get(int(user_id))
    except (ValueError, TypeError):
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role-based access control decorators
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bạn không có quyền truy cập trang này!', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_owner:
            flash('Bạn không có quyền truy cập trang này!', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_customer:
            flash('Bạn cần đăng nhập với tài khoản khách hàng để thực hiện chức năng này!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Thêm hàm helper để xử lý đường dẫn ảnh
def process_image_path(image_path):
    if not image_path:
        return '/assets/image/default-hotel.webp'
    
    # Đảm bảo đường dẫn bắt đầu từ /assets
    if 'assets' not in image_path:
        return '/assets/image/default-hotel.webp'
    
    # Cắt bỏ phần đường dẫn trước assets nếu có
    if 'assets' in image_path:
        image_path = '/assets/' + image_path.split('assets/')[-1]
    
    # Đảm bảo đường dẫn bắt đầu bằng /
    if not image_path.startswith('/'):
        image_path = '/' + image_path
        
    return image_path

# Route cho trang chủ
@app.route('/')
def home():
    app.logger.debug("Starting home route")
    user = current_user if current_user.is_authenticated else None
    app.logger.debug(f"Current user: {user}")
    
    try:
        # Fetch most picked hotels query
        most_picked_query = """
            WITH FirstRoomPrice AS (
                SELECT 
                    hotel_id,
                    price,
                    ROW_NUMBER() OVER (PARTITION BY hotel_id ORDER BY room_id) as rn
                FROM rooms
            )
            SELECT h.hotel_id, h.hotel_name, h.address_hotel, h.rating, h.descriptions, h.owner_id, r.price as min_price, hi.image_path as image_url
            FROM hotels h
            LEFT JOIN FirstRoomPrice r ON h.hotel_id = r.hotel_id AND r.rn = 1
            LEFT JOIN hotel_images hi ON h.hotel_id = hi.hotel_id AND hi.is_main = 1
            ORDER BY h.rating DESC
            LIMIT 5
        """
        
        app.logger.debug("Executing most picked hotels query")
        most_picked_result = db_session.execute(text(most_picked_query)).fetchall()
        most_picked_hotels = []
        
        # Process most picked hotels
        for hotel in most_picked_result:
            hotel_dict = hotel._asdict()
            
            main_image = db_session.execute(
                text("SELECT image_path FROM hotel_images WHERE hotel_id = :hotel_id AND is_main = 1"),
                {"hotel_id": hotel_dict['hotel_id']}
            ).fetchone()
            
            # Xử lý đường dẫn ảnh
            if main_image and main_image[0]:
                hotel_dict['image_url'] = process_image_path(main_image[0])
            else:
                hotel_dict['image_url'] = '/assets/image/default-hotel.webp'
            
            # Format location
            location_parts = hotel_dict['address_hotel'].split(',')
            if len(location_parts) >= 2:
                hotel_dict['location'] = f"{location_parts[-2].strip()}, {location_parts[-1].strip()}"
            else:
                hotel_dict['location'] = hotel_dict['address_hotel']
                
            hotel_dict['name'] = hotel_dict['hotel_name']
            most_picked_hotels.append(hotel_dict)
        
        app.logger.debug(f"Processed {len(most_picked_hotels)} most picked hotels")
        
        # Fetch list room hotels query
        list_room_query = """
            WITH FirstRoomPrice AS (
                SELECT 
                    hotel_id,
                    price,
                    ROW_NUMBER() OVER (PARTITION BY hotel_id ORDER BY room_id) as rn
                FROM rooms
            )
            SELECT h.hotel_id, h.hotel_name, h.address_hotel, h.rating, h.descriptions, h.owner_id, r.price as min_price, hi.image_path as image_url
            FROM hotels h
            LEFT JOIN FirstRoomPrice r ON h.hotel_id = r.hotel_id AND r.rn = 1
            LEFT JOIN hotel_images hi ON h.hotel_id = hi.hotel_id AND hi.is_main = 1
            ORDER BY h.rating DESC
            LIMIT 8
        """
        
        app.logger.debug("Executing list room hotels query")
        list_room_result = db_session.execute(text(list_room_query)).fetchall()
        list_room_hotels = []
        
        # Process list room hotels
        for hotel in list_room_result:
            hotel_dict = hotel._asdict()
            
            main_image = db_session.execute(
                text("SELECT image_path FROM hotel_images WHERE hotel_id = :hotel_id AND is_main = 1"),
                {"hotel_id": hotel_dict['hotel_id']}
            ).fetchone()
            
            # Xử lý đường dẫn ảnh
            if main_image and main_image[0]:
                hotel_dict['image_url'] = process_image_path(main_image[0])
            else:
                hotel_dict['image_url'] = '/assets/image/default-hotel.webp'
            
            # Format location
            location_parts = hotel_dict['address_hotel'].split(',')
            if len(location_parts) >= 2:
                hotel_dict['location'] = f"{location_parts[-2].strip()}, {location_parts[-1].strip()}"
            else:
                hotel_dict['location'] = hotel_dict['address_hotel']
                
            hotel_dict['name'] = hotel_dict['hotel_name']
            list_room_hotels.append(hotel_dict)
        
        app.logger.debug(f"Processed {len(list_room_hotels)} list room hotels")
        
        app.logger.debug("Rendering template")
        return render_template('home.html', 
                            user=user,
                            most_picked_hotels=most_picked_hotels,
                            list_room_hotels=list_room_hotels)
                            
    except Exception as e:
        app.logger.error(f"Error in home route: {str(e)}")
        return f"Error: {str(e)}", 500

# Route cho đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            remember = data.get('remember', False)
            
            if not username or not password:
                return jsonify({
                    'success': False,
                    'message': 'Vui lòng nhập đầy đủ thông tin!'
                }), 400
            
            user = db_session.query(User).filter_by(username=username).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Tài khoản không tồn tại!'
                }), 401
                
            if not check_password_hash(user.password, password):
                return jsonify({
                    'success': False,
                    'message': 'Mật khẩu không đúng!'
                }), 401
            
            # Clear any existing flash messages before login
            session.pop('_flashes', None)
            login_user(user, remember=remember)
            return jsonify({
                'success': True,
                'message': 'Đăng nhập thành công!'
            })
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Có lỗi xảy ra. Vui lòng thử lại!'
            }), 500
            
    return render_template('register.html', showLogin=True)

# Route cho đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            
            # Kiểm tra dữ liệu bắt buộc
            if not all([username, password, email]):
                return jsonify({
                    'success': False,
                    'message': 'Vui lòng điền đầy đủ thông tin bắt buộc!'
                }), 400
            
            # Kiểm tra username đã tồn tại chưa
            existing_user = db_session.query(User).filter_by(username=username).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác!'
                }), 400
            
            # Tạo user mới
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                full_name=full_name,
                phone=phone,
                role=UserRole.CUSTOMER
            )
            
            # Thêm user vào database
            db_session.add(new_user)
            db_session.commit()
            
            print(f"Đã tạo user mới: {username}")  # Debug log
            
            return jsonify({
                'success': True,
                'message': 'Đăng ký thành công!'
            })
            
        except Exception as e:
            db_session.rollback()
            print(f"Lỗi khi đăng ký: {str(e)}")  # Debug log
            return jsonify({
                'success': False,
                'message': 'Có lỗi xảy ra khi đăng ký. Vui lòng thử lại!'
            }), 500
            
    return render_template('register.html')

# Route cho đặt phòng
@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
@customer_required
def book_room(room_id):
    room = get_room_by_id(db_session, room_id)
    if not room:
        flash('Không tìm thấy phòng', 'error')
        return redirect(url_for('index'))
    
    # Lấy thông tin khách sạn
    hotel = db_session.query(Hotel).filter(Hotel.hotel_id == room.hotel_id).first()
    if not hotel:
        flash('Không tìm thấy thông tin khách sạn', 'error')
        return redirect(url_for('index'))
    
    # Lấy ảnh phòng
    room_images = db_session.execute(
        text("SELECT image_path FROM room_images WHERE room_id = :room_id"),
        {"room_id": room_id}
    ).fetchall()
    
    # Xử lý đường dẫn ảnh
    processed_images = []
    for img in room_images:
        image_path = img[0]
        if 'hotelsmanagementweb' in image_path:
            image_path = image_path[image_path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
        if not image_path.startswith('/'):
            image_path = '/' + image_path
        processed_images.append({'image_path': image_path})
    
    # Lấy services của phòng
    services = db_session.query(Service).filter(Service.room_id == room_id).all()
    
    # Phân loại services
    service_categories = {
        'in_room': [],
        'relaxation': [],
        'dining': []
    }
    
    for service in services:
        if 'room' in service.serviceName.lower():
            service_categories['in_room'].append(service)
        elif any(word in service.serviceName.lower() for word in ['spa', 'gym', 'pool', 'massage']):
            service_categories['relaxation'].append(service)
        elif any(word in service.serviceName.lower() for word in ['restaurant', 'bar', 'cafe', 'dining']):
            service_categories['dining'].append(service)
    
    # Lấy đánh giá khách sạn
    reviews = db_session.query(Review).filter(Review.hotel_id == hotel.hotel_id).order_by(Review.review_id.desc()).limit(5).all()
    avg_rating = db_session.query(func.avg(Review.rating)).filter(Review.hotel_id == hotel.hotel_id).scalar() or 0
        
    if request.method == 'POST':
        check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d')
        check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d')
        num_guests = int(request.form.get('num_guests', 1))
        special_requests = request.form.get('special_requests', '')
        
        if check_in >= check_out:
            flash('Ngày check-out phải sau ngày check-in', 'error')
            return redirect(url_for('book_room', room_id=room_id))
            
        # Tính tổng giá
        nights = (check_out - check_in).days
        total_price = room.price * nights
        
        try:
            # Tạo booking
            booking = Booking(
                user_id=current_user.user_id,
                room_id=room_id,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price,
                status='pending',
                created_at=datetime.now()
            )
            db_session.add(booking)
            db_session.commit()
            
            # Tạo payment
            payment = Payment(
                booking_id=booking.booking_id,
                amount=total_price,
                payment_method='...',
                status='pending',
                user_id=current_user.user_id,
                created_at=datetime.now()
            )
            db_session.add(payment)
            db_session.commit()
            
            # Cập nhật số lượng phòng trống
            room.availableRooms -= 1
            db_session.commit()
            
            flash('Đặt phòng thành công!', 'success')
            return redirect(url_for('booking_confirmation', booking_id=booking.booking_id))
            
        except Exception as e:
            db_session.rollback()
            flash('Có lỗi xảy ra khi đặt phòng', 'error')
            return redirect(url_for('book_room', room_id=room_id))
            
    return render_template('booking.html',
                         hotel=hotel,
                         room=room,
                         room_images=processed_images,
                         services=service_categories,
                         reviews=reviews,
                         avg_rating=round(avg_rating, 1))

# Route cho xem chi tiết đặt phòng
@app.route('/booking/<int:booking_id>')
@login_required
def booking_details(booking_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    booking = get_booking_by_id(db_session, booking_id)
    if not booking or booking.user_id != current_user.user_id:
        flash('Không tìm thấy thông tin đặt phòng', 'error')
        return redirect(url_for('index'))
    return render_template('booking_details.html', booking=booking)

# Route cho xem lịch sử đặt phòng
@app.route('/user/my-bookings')
@login_required
def my_bookings():
    # Lấy tất cả booking của user hiện tại
    bookings = db_session.query(Booking).filter_by(user_id=current_user.id)\
        .order_by(Booking.created_at.desc()).all()
    
    return render_template('my_bookings.html', bookings=bookings)

# Route cho đánh giá khách sạn
@app.route('/hotel/<int:hotel_id>/review', methods=['POST'])
@login_required
def review_hotel(hotel_id):
    rating = float(request.form.get('rating'))
    comment = request.form.get('comment')
    
    if not rating or rating < 0 or rating > 5:
        flash('Đánh giá không hợp lệ', 'error')
        return redirect(url_for('hotel_details', hotel_id=hotel_id))
        
    try:
        review = create_review(db_session, session['user_id'], hotel_id, rating, comment)
        flash('Đánh giá thành công!', 'success')
    except Exception as e:
        db_session.rollback()
        flash('Có lỗi xảy ra khi đánh giá', 'error')
        
    return redirect(url_for('hotel_details', hotel_id=hotel_id))

# Route cho xem chi tiết khách sạn
@app.route('/hotel/<int:hotel_id>')
def hotel_details(hotel_id):
    try:
        hotel = db_session.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()
        if not hotel:
            abort(404)
        
        # Lấy danh sách phòng của khách sạn
        rooms = db_session.query(Room).filter(Room.hotel_id == hotel_id).all()
        
        # Lấy phòng đầu tiên để hiển thị mặc định
        first_room = rooms[0] if rooms else None
        
        # Lấy hình ảnh của khách sạn
        hotel_images = db_session.execute(
            text("SELECT image_path FROM hotel_images WHERE hotel_id = :hotel_id"),
            {"hotel_id": hotel_id}
        ).fetchall()
        
        hotel_image_urls = []
        for img in hotel_images:
            image_path = img[0]
            if 'hotelsmanagementweb' in image_path:
                image_path = image_path[image_path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
            if not image_path.startswith('/'):
                image_path = '/' + image_path
            hotel_image_urls.append(image_path)
        
        if not hotel_image_urls:
            hotel_image_urls = ['/assets/image/default-hotel.webp']
        
        # Format location từ address_hotel
        location_parts = hotel.address_hotel.split(',')
        if len(location_parts) >= 2:
            hotel.location = f"{location_parts[-2].strip()}, {location_parts[-1].strip()}"
        else:
            hotel.location = hotel.address_hotel
        
        # Lấy đánh giá khách sạn và sắp xếp theo review_id
        reviews = db_session.query(Review).filter(Review.hotel_id == hotel_id).order_by(Review.review_id.desc()).limit(5).all()
        
        # Thêm thông tin cho mỗi phòng
        processed_rooms = []
        for room in rooms:
            # Tính giá sau khi giảm 10%
            original_price = room.price
            discount_percent = 10
            discounted_price = int(original_price * (1 - discount_percent/100))
            
            room_dict = {
                'room_id': room.room_id,
                'room_type': room.room_type,
                'price': discounted_price,  # Giá đã giảm
                'availableRooms': room.availableRooms,
                'original_price': original_price,  # Giá gốc
                'discount_percent': discount_percent,  # Phần trăm giảm giá
                'max_guests': 2,
                'room_size': 30,
                'view_type': "City View",
                'bed_type': "1 King Bed",
                'services': []
            }
            
            # Lấy tất cả ảnh của phòng
            room_images = db_session.execute(
                text("SELECT image_path FROM room_images WHERE room_id = :room_id"),
                {"room_id": room.room_id}
            ).fetchall()
            
            room_dict['images'] = []
            # Xử lý đường dẫn ảnh
            for img in room_images:
                image_path = img[0]
                if 'hotelsmanagementweb' in image_path:
                    image_path = image_path[image_path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
                if not image_path.startswith('/'):
                    image_path = '/' + image_path
                room_dict['images'].append(image_path)
                
            # Nếu không có ảnh, sử dụng ảnh mặc định
            if not room_dict['images']:
                room_dict['images'] = ['/assets/image/default-room.webp']
                
            # Sử dụng ảnh đầu tiên làm ảnh chính
            room_dict['image_url'] = room_dict['images'][0]
                
            # Lấy danh sách dịch vụ của phòng
            services = db_session.query(Service).filter(Service.room_id == room.room_id).all()
            room_dict['services'] = [
                {
                    'serviceName': service.serviceName,
                    'icon': 'fas fa-check'
                }
                for service in services
            ]
            
            processed_rooms.append(room_dict)
        
        if first_room:
            first_room_dict = processed_rooms[0]
        else:
            first_room_dict = None
        
        return render_template('detailroom.html', 
                             hotel=hotel,
                             images=hotel_image_urls,
                             rooms=processed_rooms,
                             room=first_room_dict,
                             reviews=reviews)
                             
    except Exception as e:
        app.logger.error(f"Error in hotel_details: {str(e)}")
        db_session.rollback()
        return "Có lỗi xảy ra khi tải thông tin khách sạn", 500

# Route cho đăng xuất
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flask.session.clear()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/user')
@login_required
def user_profile():
    return render_template('user.html', user=current_user)

@app.route('/api/room-images/<int:room_id>')
def get_room_images(room_id):
    # Lấy tất cả ảnh của phòng
    images = db_session.execute(
        text("SELECT image_path FROM room_images WHERE room_id = :room_id"),
        {"room_id": room_id}
    ).fetchall()
    
    image_urls = []
    for img in images:
        path = img[0]
        if 'hotelsmanagementweb' in path:
            # Lấy đường dẫn tương đối từ hotelsmanagementweb
            path = path[path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
            # Chuyển đổi dấu gạch chéo ngược thành dấu gạch chéo xuôi
            path = path.replace('\\', '/')
            # Đảm bảo đường dẫn bắt đầu bằng /
            if not path.startswith('/'):
                path = '/' + path
        image_urls.append(path)
    
    # Nếu không có ảnh, trả về ảnh mặc định
    if not image_urls:
        image_urls = ['/assets/image/default-room.webp']
    
    return jsonify(image_urls)

@app.route('/api/room-services/<int:room_id>')
def get_room_services(room_id):
    services = db_session.query(Service).filter(Service.room_id == room_id).all()
    
    service_icons = {
        'Breakfast': 'fas fa-coffee',
        'Dinner': 'fas fa-utensils',
        'Free WiFi': 'fas fa-wifi',
        'Gym Access': 'fas fa-dumbbell',
        'Pool Access': 'fas fa-swimming-pool',
        'Room Service': 'fas fa-concierge-bell',
        'Airport Transfer': 'fas fa-shuttle-van',
        'Spa Access': 'fas fa-spa',
        'Free Parking': 'fas fa-parking',
        'Beach Access': 'fas fa-umbrella-beach'
    }
    
    service_list = []
    for service in services:
        service_list.append({
            'name': service.serviceName,
            'icon': service_icons.get(service.serviceName, 'fas fa-check'),
            'is_included': True  # You can modify this based on your logic
        })
    
    return jsonify(service_list)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    pass  # hoặc có thể thêm logic sau

@app.route('/payment', methods=['POST'])
@login_required
def create_payment():
    # Lấy dữ liệu từ form gửi lên
    hotel_id = request.form.get('hotel_id')
    room_id = request.form.get('room_id')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    num_rooms = int(request.form.get('num_rooms', 1))
    num_nights = int(request.form.get('num_nights'))
    total_price = float(request.form.get('total_price'))
    user_id = current_user.user_id  # Lấy user_id từ user đã đăng nhập

    # Lưu vào DB
    booking = Booking(
        user_id=user_id,
        room_id=room_id,
        check_in=datetime.strptime(check_in, '%Y-%m-%d'),
        check_out=datetime.strptime(check_out, '%Y-%m-%d'),
        total_price=total_price,
        num_rooms=num_rooms,  # Lưu đúng số phòng
        status='pending',
        created_at=datetime.now()
    )
    db_session.add(booking)
    db_session.commit()

    # Lấy thông tin để render ra payment.html
    room = Room.query.get(room_id)
    hotel = Hotel.query.get(hotel_id)
    return render_template('payment.html', booking=booking, room=room, hotel=hotel, nights=num_nights)

@app.route('/booking/confirmation/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    booking = db_session.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        abort(404)
    if booking.user_id != current_user.id:
        abort(403)
    
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/search', methods=['POST'])
def search_hotels():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location', 'check_in_date', 'check_out_date', 'required_rooms']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Parse dates
        try:
            check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d')
            check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Validate dates
        if check_in < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return jsonify({'error': 'Check-in date cannot be in the past'}), 400
        if check_out <= check_in:
            return jsonify({'error': 'Check-out date must be after check-in date'}), 400

        # Calculate number of nights
        nights = (check_out - check_in).days

        # Build the SQL query
        query = """
        WITH RoomAvailability AS (
            SELECT 
                h.hotel_id,
                h.hotel_name,
                h.address_hotel as location,
                h.rating,
                COUNT(DISTINCT r.room_id) as total_rooms,
                COUNT(DISTINCT CASE 
                    WHEN b.booking_id IS NULL 
                    OR (b.check_in >= :check_out OR b.check_out <= :check_in)
                    THEN r.room_id 
                END) as available_rooms,
                MIN(r.price) as min_price
            FROM hotels h
            LEFT JOIN rooms r ON h.hotel_id = r.hotel_id
            LEFT JOIN bookings b ON r.room_id = b.room_id
            WHERE h.address_hotel LIKE :location
            GROUP BY h.hotel_id, h.hotel_name, h.address_hotel, h.rating
            HAVING available_rooms >= :required_rooms
        )
        SELECT 
            hotel_id,
            hotel_name,
            location,
            rating,
            min_price,
            available_rooms,
            total_rooms
        FROM RoomAvailability
        ORDER BY rating DESC, min_price ASC
        """

        # Execute query with parameters
        result = db_session.execute(
            text(query), 
            {
                'location': f'%{data["location"]}%',
                'check_in': check_in,
                'check_out': check_out,
                'required_rooms': data['required_rooms']
            }
        )

        # Convert result to list of dictionaries
        hotels = []
        for row in result:
            # Get main image for hotel
            main_image = db_session.execute(
                text("SELECT image_path FROM hotel_images WHERE hotel_id = :hotel_id AND is_main = 1"),
                {"hotel_id": row.hotel_id}
            ).fetchone()
            
            # Process image path
            image_path = None
            if main_image and main_image[0]:
                image_path = main_image[0]
                if 'hotelsmanagementweb' in image_path:
                    image_path = image_path[image_path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
                if not image_path.startswith('/'):
                    image_path = '/' + image_path
            
            hotels.append({
                'hotel_id': row.hotel_id,
                'hotel_name': row.hotel_name,
                'location': row.location,
                'rating': float(row.rating),
                'image_path': image_path or '/assets/image/default-room.jpg',
                'min_price': float(row.min_price) if row.min_price else 0,
                'available_rooms': row.available_rooms,
                'total_rooms': row.total_rooms
            })

        return jsonify({
            'hotels': hotels,
            'total': len(hotels),
            'nights': nights
        })

    except Exception as e:
        print(f"Error in search_hotels: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/search-by-name', methods=['GET'])
def search_hotels_by_name():
    try:
        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({'hotels': [], 'total': 0})

        # Build the SQL query
        query = """
        SELECT 
            h.hotel_id,
            h.hotel_name,
            h.address_hotel as location,
            h.rating,
            MIN(r.price) as min_price,
            COUNT(DISTINCT r.room_id) as total_rooms,
            COUNT(DISTINCT CASE WHEN r.availableRooms > 0 THEN r.room_id END) as available_rooms
        FROM hotels h
        LEFT JOIN rooms r ON h.hotel_id = r.hotel_id
        WHERE LOWER(h.hotel_name) LIKE LOWER(:search_term)
        GROUP BY h.hotel_id, h.hotel_name, h.address_hotel, h.rating
        ORDER BY h.rating DESC
        LIMIT 10
        """

        # Execute query
        result = db_session.execute(
            text(query),
            {'search_term': f'%{search_term}%'}
        )

        # Convert result to list of dictionaries
        hotels = []
        for row in result:
            # Get main image for hotel
            main_image = db_session.execute(
                text("SELECT image_path FROM hotel_images WHERE hotel_id = :hotel_id AND is_main = 1"),
                {"hotel_id": row.hotel_id}
            ).fetchone()
            
            # Process image path
            image_path = None
            if main_image and main_image[0]:
                image_path = main_image[0]
                if 'hotelsmanagementweb' in image_path:
                    image_path = image_path[image_path.index('hotelsmanagementweb')+len('hotelsmanagementweb'):]
                if not image_path.startswith('/'):
                    image_path = '/' + image_path
            
            hotels.append({
                'hotel_id': row.hotel_id,
                'hotel_name': row.hotel_name,
                'location': row.location,
                'rating': float(row.rating),
                'image_path': image_path or '/assets/image/default-room.jpg',
                'min_price': float(row.min_price) if row.min_price else 0,
                'available_rooms': row.available_rooms or 0,
                'total_rooms': row.total_rooms or 0
            })

        return jsonify({
            'hotels': hotels,
            'total': len(hotels)
        })

    except Exception as e:
        print(f"Error in search_hotels_by_name: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Route cho quản lý khách sạn (chỉ dành cho owner)
@app.route('/manage-hotels')
@owner_required
def manage_hotels():
    hotels = db_session.query(Hotel).filter(Hotel.owner_id == current_user.user_id).all()
    return render_template('manage_hotels.html', hotels=hotels)

# Route cho quản lý người dùng (chỉ dành cho admin)
@app.route('/manage-users')
@admin_required
def manage_users():
    users = db_session.query(User).all()
    return render_template('manage_users.html', users=users)

# Route cho thanh toán (chỉ dành cho customer)
@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@customer_required
def payment(booking_id):
    try:
        # Get booking information
        booking = db_session.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            flash('Booking not found', 'error')
            return redirect(url_for('my_bookings'))
            
        # Check if booking belongs to current user
        if booking.user_id != current_user.id:
            flash('Unauthorized access', 'error')
            return redirect(url_for('my_bookings'))
            
        # Get hotel and room information
        hotel = db_session.query(Hotel).filter_by(hotel_id=booking.hotel_id).first()
        room = db_session.query(Room).filter_by(room_id=booking.room_id).first()
        
        if not hotel or not room:
            flash('Hotel or room information not found', 'error')
            return redirect(url_for('my_bookings'))
            
        # Calculate number of nights
        nights = (booking.check_out - booking.check_in).days
        
        # For GET request, show payment page
        if request.method == 'GET':
            return render_template('payment.html',
                                booking=booking,
                                hotel=hotel,
                                room=room,
                                nights=nights)
                                
        # For POST request, process payment
        payment_method = request.form.get('payment_method')
        
        if payment_method == 'credit_card':
            # Validate credit card info
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')
            cardholder_name = request.form.get('cardholder_name')
            
            if not all([card_number, expiry_date, cvv, cardholder_name]):
                flash('Please fill in all card details', 'error')
                return redirect(url_for('payment', booking_id=booking_id))
                
            # Here you would integrate with a payment gateway
            # For demo purposes, we'll just mark the payment as successful
            
        elif payment_method == 'bank_transfer':
            # Generate bank transfer information
            pass
            
        elif payment_method == 'momo':
            # Integrate with MoMo payment
            pass
            
        else:
            flash('Invalid payment method', 'error')
            return redirect(url_for('payment', booking_id=booking_id))
            
        # Update booking and payment status
        booking.status = 'confirmed'
        payment = Payment(
            booking_id=bookings.booking_id,
            amount=booking.total_price,
            payment_method=payment_method,
            status='completed',
            user_id=current_user.id
        )
        
        db_session.add(payment)
        db_session.commit()
        
        flash('Payment successful! Your booking is confirmed.', 'success')
        return redirect(url_for('booking_confirmation', booking_id=booking_id))
        
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"Error processing payment: {str(e)}")
        flash('An error occurred while processing your payment. Please try again.', 'error')
        return redirect(url_for('payment', booking_id=booking_id))

# Route cho thêm/sửa khách sạn (chỉ dành cho owner)
@app.route('/hotel/edit/<int:hotel_id>', methods=['GET', 'POST'])
@owner_required
def edit_hotel(hotel_id):
    hotel = db_session.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()
    
    # Kiểm tra xem owner có sở hữu khách sạn này không
    if hotel and hotel.owner_id != current_user.user_id:
        flash('Bạn không có quyền chỉnh sửa khách sạn này!', 'error')
        return redirect(url_for('manage_hotels'))
    
    if request.method == 'POST':
        # ... hotel editing code ...
        pass
        
    return render_template('edit_hotel.html', hotel=hotel)

# Route cho xem thống kê (dành cho owner và admin)
@app.route('/statistics')
@login_required
def statistics():
    if not (current_user.is_admin or current_user.is_owner):
        flash('Bạn không có quyền truy cập trang này!', 'error')
        return redirect(url_for('home'))
        
    stats = {}
    
    if current_user.is_admin:
        # Thống kê toàn bộ hệ thống
        stats['total_users'] = db_session.query(User).count()
        stats['total_hotels'] = db_session.query(Hotel).count()
        stats['total_bookings'] = db_session.query(Booking).count()
    else:
        # Thống kê cho owner
        hotels = db_session.query(Hotel).filter(Hotel.owner_id == current_user.user_id).all()
        hotel_ids = [hotel.hotel_id for hotel in hotels]
        stats['total_hotels'] = len(hotels)
        stats['total_bookings'] = db_session.query(Booking).join(Room).filter(Room.hotel_id.in_(hotel_ids)).count()
        
    return render_template('statistics.html', stats=stats)

# Route cho quên mật khẩu
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db_session.query(User).filter_by(email=email).first()
        
        if user:
            # Lấy hoặc tạo bản ghi bảo mật cho user
            security = user.security
            if not security:
                security = UserSecurity(user_id=user.user_id)
                db_session.add(security)
            
            # Tạo token reset mật khẩu
            token = secrets.token_urlsafe(32)
            security.password_reset_token = token
            security.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
            db_session.commit()
            
            # Gửi email reset mật khẩu
            reset_url = url_for('reset_password', token=token, _external=True)
            send_password_reset_email(user.email, reset_url)
            
            flash('Vui lòng kiểm tra email để đặt lại mật khẩu!', 'success')
        else:
            flash('Email không tồn tại trong hệ thống!', 'error')
    
    return render_template('forgot_password.html')

# Route cho đặt lại mật khẩu
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    security = db_session.query(UserSecurity).filter_by(password_reset_token=token).first()
    
    if not security or security.password_reset_expires < datetime.utcnow():
        flash('Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn!', 'error')
        return redirect(url_for('login'))
    
    user = security.user
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Mật khẩu không khớp!', 'error')
            return redirect(url_for('reset_password', token=token))
        
        user.password = generate_password_hash(password)
        security.password_reset_token = None
        security.password_reset_expires = None
        db_session.commit()
        
        flash('Đặt lại mật khẩu thành công!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

# Route cho xác thực email
@app.route('/verify-email/<token>')
def verify_email(token):
    security = db_session.query(UserSecurity).filter_by(email_verification_token=token).first()
    
    if security:
        security.email_verified = True
        security.email_verification_token = None
        db_session.commit()
        flash('Xác thực email thành công!', 'success')
    else:
        flash('Link xác thực không hợp lệ!', 'error')
    
    return redirect(url_for('login'))

@app.route('/user/my-reviews')
@login_required
def my_reviews():
    # Lấy tất cả review của user hiện tại
    reviews = db_session.query(Review).filter_by(user_id=current_user.id)\
        .order_by(Review.created_at.desc()).all()
    
    return render_template('my_reviews.html', reviews=reviews)

@app.route('/user/account-settings')
@login_required
def account_settings():
    return render_template('account_settings.html', user=current_user)

@app.route('/user/update-profile', methods=['POST'])
@login_required
def update_profile():
    try:
        data = request.form
        user = current_user
        
        # Cập nhật thông tin user
        user.full_name = data.get('full_name')
        user.email = data.get('email')
        user.phone = data.get('phone')
        
        db_session.commit()
        
        flash('Cập nhật thông tin thành công!', 'success')
    except Exception as e:
        db_session.rollback()
        flash('Có lỗi xảy ra khi cập nhật thông tin!', 'error')
        
    return redirect(url_for('account_settings'))

@app.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        try:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # Kiểm tra mật khẩu hiện tại
            if not check_password_hash(current_user.password, current_password):
                flash('Mật khẩu hiện tại không đúng!', 'error')
                return redirect(url_for('change_password'))
            
            # Kiểm tra mật khẩu mới và xác nhận
            if new_password != confirm_password:
                flash('Mật khẩu mới không khớp!', 'error')
                return redirect(url_for('change_password'))
            
            # Cập nhật mật khẩu mới
            current_user.password = generate_password_hash(new_password)
            db_session.commit()
            
            flash('Đổi mật khẩu thành công!', 'success')
            return redirect(url_for('account_settings'))
            
        except Exception as e:
            db_session.rollback()
            flash('Có lỗi xảy ra khi đổi mật khẩu!', 'error')
            return redirect(url_for('change_password'))
    
    return render_template('change_password.html')

VNPAY_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNP_TMN_CODE = 'IQRCRXK8'
VNP_HASH_SECRET = 'STDTDERBNDXT2LRBW1U4B59N72ZWWXDF'
VNP_RETURN_URL = 'http://localhost:5000/vnpay_return'

def build_vnpay_query_and_hash(vnp_params, secret_key):
    sorted_items = sorted(
        [(k, v) for k, v in vnp_params.items() if v not in [None, '', 'undefined']],
        key=lambda x: x[0]
    )
    query_string = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_items])
    hash_data = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_items])
    vnp_secure_hash = hmac.new(
        secret_key.encode('utf-8'),
        hash_data.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()
    return query_string, vnp_secure_hash

@app.route('/vnpay_pay', methods=['POST'])
@login_required
def vnpay_pay():
    amount = float(request.form.get('total_price', 0))
    amount_vnd = int(amount)
    if amount_vnd < 5000 or amount_vnd >= 1_000_000_000:
        return "Số tiền không hợp lệ (từ 5,000 đến dưới 1 tỷ đồng)", 400
    order_id = 'ORDER' + datetime.now().strftime('%Y%m%d%H%M%S')
    order_desc = f"Thanh toán đơn hàng {order_id}"
    user_ip = request.remote_addr or '127.0.0.1'
    vnp_params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': VNP_TMN_CODE,
        'vnp_Amount': str(amount_vnd * 100),
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': order_id,
        'vnp_OrderInfo': order_desc,
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': VNP_RETURN_URL,
        'vnp_IpAddr': user_ip,
        'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
    }
    query_string, vnp_secure_hash = build_vnpay_query_and_hash(vnp_params, VNP_HASH_SECRET)
    # Lưu thông tin vào bảng payment
    payment = Payment(
        txn_ref=order_id,
        amount=amount_vnd,
        payment_method='vnpay',
        payment_status='pending',
        secure_hash=vnp_secure_hash,
        created_at=datetime.now(),
        # booking_id=booking_id  # Bỏ comment nếu có booking_id, nếu không thì để None
    )
    db_session.add(payment)
    db_session.commit()
    payment_url = f"{VNPAY_URL}?{query_string}&vnp_SecureHash={vnp_secure_hash}"
    return redirect(payment_url)

@app.route('/vnpay_return')
def vnpay_return():
    vnp_ResponseCode = request.args.get('vnp_ResponseCode')
    vnp_TxnRef = request.args.get('vnp_TxnRef')
    from models import Payment
    payment = db_session.query(Payment).filter_by(txn_ref=vnp_TxnRef).first()
    if payment:
        payment.response_code = vnp_ResponseCode
        if vnp_ResponseCode == '00':
            payment.payment_status = 'success'
        else:
            payment.payment_status = 'failed'
        payment.pay_date = datetime.now()
        db_session.commit()
    if vnp_ResponseCode == '00':
        message = 'Thanh toán thành công qua VNPAY!'
    else:
        message = 'Thanh toán thất bại hoặc bị hủy!'
    return f'''
    <script>
        alert("{message}");
        window.location.href = "/";
    </script>
    '''

@app.route('/api/user/info')
@login_required
def api_user_info():
    return jsonify({
        "username": current_user.username,
        "full_name": getattr(current_user, 'full_name', ''),
        "first_name": getattr(current_user, 'first_name', ''),
        "last_name": getattr(current_user, 'last_name', ''),
        "email": current_user.email,
        "phone": getattr(current_user, 'phone', ''),
        "role": getattr(current_user, 'role', 'User')
    })

@app.route('/api/user/bookings')
@login_required
def api_user_bookings():
    bookings = db_session.query(Booking).filter_by(user_id=current_user.user_id).all()
    result = []
    for b in bookings:
        result.append({
            "id": b.booking_id,
            "hotel_name": b.hotel.hotel_name if hasattr(b, 'hotel') and b.hotel else '',
            "hotel_location": b.hotel.address_hotel if hasattr(b, 'hotel') and b.hotel else '',
            "hotel_address": b.hotel.address_hotel if hasattr(b, 'hotel') and b.hotel else '',
            "check_in": b.check_in.strftime('%Y-%m-%d') if b.check_in else '',
            "check_out": b.check_out.strftime('%Y-%m-%d') if b.check_out else '',
            "initial_payment": getattr(b, 'initial_payment', 0),
            "total_payment": getattr(b, 'total_price', 0),
            "status": b.status
        })
    return jsonify({"bookings": result})

@app.route('/api/user/notifications')
@login_required
def api_user_notifications():
    # Giả sử bạn có bảng Notification với user_id
    notifications = db_session.execute(
        text("SELECT id, type, message, read, created_at FROM notifications WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": current_user.user_id}
    ).fetchall()
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "type": n.type,
            "message": n.message,
            "read": n.read,
            "created_at": n.created_at.isoformat() if n.created_at else ''
        })
    return jsonify({"notifications": result})

@app.route('/api/user/transactions')
@login_required
def api_user_transactions():
    # Giả sử bạn có bảng Payment với user_id
    transactions = db_session.query(Payment).filter_by(user_id=current_user.user_id).order_by(Payment.created_at.desc()).all()
    result = []
    for t in transactions:
        result.append({
            "id": getattr(t, 'txn_ref', t.id),
            "date": t.created_at.strftime('%Y-%m-%d') if t.created_at else '',
            "amount": t.amount,
            "hotel_name": t.booking.hotel.hotel_name if hasattr(t, 'booking') and t.booking and hasattr(t.booking, 'hotel') and t.booking.hotel else '',
            "nights": (t.booking.check_out - t.booking.check_in).days if hasattr(t, 'booking') and t.booking and t.booking.check_in and t.booking.check_out else 1,
            "status": t.payment_status if hasattr(t, 'payment_status') else t.status,
            "room_rate": getattr(t, 'room_rate', 0),
            "taxes": getattr(t, 'taxes', 0),
            "payment_method": t.payment_method,
            "last_four": str(t.card_number)[-4:] if hasattr(t, 'card_number') and t.card_number else ''
        })
    return jsonify({"transactions": result})

if __name__ == '__main__':
    try:
        # Tạo database và bảng
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        
    app.run(debug=True) 