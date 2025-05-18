from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import Session
from models import User, Hotel, Room, Service, Review, Booking, Payment
from flask_mail import Message
from flask import current_app
import os

def create_user(db: Session, username: str, password: str, email: str, full_name: str = None, phone: str = None):
    hashed_password = generate_password_hash(password)
    user = User(
        username=username,
        password=hashed_password,
        email=email,
        full_name=full_name,
        phone=phone,
        is_admin=0
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def create_guest(db: Session, guest_name: str, email: str, phone: str, nationality: str = None):
    guest = Guest(
        guest_name=guest_name,
        email=email,
        phone=phone,
        nationality=nationality
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

def get_available_rooms(db: Session, hotel_id: int = None, room_type: str = None):
    query = db.query(Room).filter(Room.availableRooms > 0)
    
    if hotel_id:
        query = query.filter(Room.hotel_id == hotel_id)
    if room_type:
        query = query.filter(Room.room_type == room_type)
        
    return query.all()

def create_booking(db: Session, user_id: int, room_id: int, check_in: datetime, check_out: datetime, total_price: float, num_rooms: int = 1):
    booking = Booking(
        user_id=user_id,
        room_id=room_id,
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
        num_rooms=num_rooms,
        status='pending'
    )
    db.add(booking)
    room = db.query(Room).filter(Room.room_id == room_id).first()
    if room and room.availableRooms is not None and room.availableRooms >= num_rooms:
        room.availableRooms -= num_rooms
    db.commit()
    db.refresh(booking)
    return booking

def create_payment(db: Session, booking_id: int, amount: int, payment_method: str, user_id: int):
    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        payment_method=payment_method,
        payment_status='pending',
        user_id=user_id
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def create_review(db: Session, user_id: int, hotel_id: int, rating: float, comment: str):
    review = Review(
        user_id=user_id,
        hotel_id=hotel_id,
        rating=rating,
        comment=comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_hotel_by_id(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.hotel_id == hotel_id).first()

def get_room_by_id(db: Session, room_id: int):
    return db.query(Room).filter(Room.room_id == room_id).first()

def get_guest_by_id(db: Session, guest_id: int):
    return db.query(Guest).filter(Guest.id == guest_id).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.booking_id == booking_id).first()

def get_user_bookings(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_hotel_reviews(db: Session, hotel_id: int):
    return db.query(Review).filter(Review.hotel_id == hotel_id).all()

def send_email(to, subject, template):
    """
    Hàm tiện ích để gửi email
    """
    try:
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=current_app.config['MAIL_USERNAME']
        )
        current_app.extensions['mail'].send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def send_verification_email(email, verification_url):
    """
    Gửi email xác thực tài khoản
    """
    subject = "Xác thực tài khoản - HaNoi Booking"
    template = f"""
    <h1>Xác thực tài khoản của bạn</h1>
    <p>Cảm ơn bạn đã đăng ký tài khoản tại HaNoi Booking. Vui lòng click vào link bên dưới để xác thực email của bạn:</p>
    <p><a href="{verification_url}">Xác thực email</a></p>
    <p>Link này sẽ hết hạn sau 24 giờ.</p>
    <p>Nếu bạn không yêu cầu tạo tài khoản, vui lòng bỏ qua email này.</p>
    """
    return send_email(email, subject, template)

def send_password_reset_email(email, reset_url):
    """
    Gửi email đặt lại mật khẩu
    """
    subject = "Đặt lại mật khẩu - HaNoi Booking"
    template = f"""
    <h1>Đặt lại mật khẩu</h1>
    <p>Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của mình. Vui lòng click vào link bên dưới để đặt lại mật khẩu:</p>
    <p><a href="{reset_url}">Đặt lại mật khẩu</a></p>
    <p>Link này sẽ hết hạn sau 1 giờ.</p>
    <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
    """
    return send_email(email, subject, template) 