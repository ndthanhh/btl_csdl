from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum, BigInteger
from sqlalchemy.orm import relationship
from config import Base
from flask_login import UserMixin
from datetime import datetime
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    OWNER = "owner"
    CUSTOMER = "customer"

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    security = relationship("UserSecurity", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    hotels = relationship("Hotel", back_populates="owner")
    
    def get_id(self):
        """Return the user ID as a unicode string."""
        return str(self.user_id)
    
    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
        
    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def has_role(self, role):
        """Check if user has the specified role"""
        return self.role == role
        
    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN
        
    @property
    def is_owner(self):
        """Check if user is a hotel owner"""
        return self.role == UserRole.OWNER
        
    @property
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == UserRole.CUSTOMER

class UserSecurity(Base):
    __tablename__ = 'user_security'
    
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(100))
    password_reset_token = Column(String(100))
    password_reset_expires = Column(DateTime)
    last_login = Column(DateTime)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="security")

class Hotel(Base):
    __tablename__ = 'hotels'
    
    hotel_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String(50), nullable=False)
    address_hotel = Column(String(150), nullable=False)
    tel = Column(String(20), nullable=False)
    rating = Column(Float)
    descriptions = Column(String(1000))
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")

class Room(Base):
    __tablename__ = 'rooms'
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_type = Column(String(25), nullable=False)
    availableRooms = Column(Integer)
    price = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.hotel_id'), nullable=False)
    
    # Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    services = relationship("Service", back_populates="room")
    bookings = relationship("Booking", back_populates="room")
    images = relationship("RoomImage", back_populates="room")

class Service(Base):
    __tablename__ = 'services'
    
    id_service = Column(Integer, primary_key=True, autoincrement=True)
    serviceName = Column(String(255), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.room_id'), nullable=False)
    
    # Relationships
    room = relationship("Room", back_populates="services")

class Review(Base):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    rating = Column(Float)
    comment = Column(String(200))
    hotel_id = Column(Integer, ForeignKey('hotels.hotel_id'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")

class Booking(Base):
    __tablename__ = 'bookings'
    
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.room_id'), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    num_rooms = Column(Integer, nullable=False, default=1)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)

class Payment(Base):
    __tablename__ = 'payment'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    txn_ref = Column(String(100))
    amount = Column(BigInteger)
    bank_code = Column(String(50))
    pay_date = Column(DateTime)
    response_code = Column(String(10))
    payment_status = Column(String(50))
    secure_hash = Column(Text)
    payment_method = Column(String(50))
    
    # Relationships
    booking = relationship("Booking", back_populates="payment")

class RoomImage(Base):
    __tablename__ = 'room_images'
    
    image_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.room_id'), nullable=False)
    image_path = Column(String(255), nullable=False)
    
    # Relationship
    room = relationship('Room', back_populates='images')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    type = Column(String(50))
    message = Column(String(255))
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="notifications") 