from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Numeric, Enum, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Optional Enum for payment status
class PaymentStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"

class PaymentMethod(enum.Enum):
    credit_card = "credit_card"
    paypal = "paypal"
    alipay = "alipay"
    wechat_pay = "wechat_pay"
    apple_pay = "apple_pay"

class UserRole(enum.Enum):
    user = "user"
    merchant = "merchant"
    admin = "admin"

class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class MerchantCategory(enum.Enum):
    ktv = "KTV"
    massage = "Massage"
    art = "Art"
    escape_room = "Escape Room"
    yoga = "Yoga"
    language_class = "Language Class"
    dance_studio = "Dance Studio"
    cooking = "Cooking"
    workshop = "Workshop"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # ✅ now unique
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)  # for storing active refresh token (or hashed)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    merchant_profile = relationship("Merchant", back_populates="user", uselist=False)

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    category = Column(Enum(MerchantCategory), nullable=False)

    user = relationship("User", back_populates="merchant_profile")
    themes = relationship("Theme", back_populates="merchant")

class Theme(Base):
    __tablename__ = "themes"

    id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey("merchants.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)

    merchant = relationship("Merchant", back_populates="themes")
    slots = relationship("Slot", back_populates="theme")
    reviews = relationship("Review", back_populates="theme")

class Slot(Base):
    __tablename__ = "slots"

    id = Column(String, primary_key=True)
    theme_id = Column(String, ForeignKey("themes.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    
    theme = relationship("Theme", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")

    __table_args__ = (
        CheckConstraint("capacity >= 0", name="check_slot_capacity_non_negative"),
    )

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    slot_id = Column(String, ForeignKey("slots.id"), nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    slot = relationship("Slot", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)
    review = relationship("Review", back_populates="booking", uselist=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    payment_intent_id = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
    booking = relationship("Booking", back_populates="payment")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False, unique=True) 
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    theme_id = Column(String, ForeignKey("themes.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    theme = relationship("Theme", back_populates="reviews")
    booking = relationship("Booking", back_populates="review")

