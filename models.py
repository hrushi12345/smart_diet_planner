from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Enum
import uuid
from datetime import datetime

db = SQLAlchemy()

class UserAccount(db.Model):
    __tablename__ = 'user_account'

    userId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    createdAt = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    profile = db.relationship("UserProfile", backref="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    profileId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    userId = db.Column(db.String(36), db.ForeignKey('user_account.userId'), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(Enum('Male', 'Female', 'Other', name="gender_enum"), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    activityLevel = db.Column(Enum('Low', 'Medium', 'High', name="activity_enum"), nullable=False)
    goal = db.Column(Enum('Weight Loss', 'Muscle Gain', 'Maintenance', name="goal_enum"), nullable=False)
    createdAt = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class UserDietRecommendation(db.Model):
    __tablename__ = 'user_diet_recommendation'

    recommendationId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    userId = db.Column(db.String(36), db.ForeignKey('user_account.userId'), nullable=False)
    dietPlanId = db.Column(db.String(36), nullable=False)
    assignedDate = db.Column(db.Date, default=datetime.utcnow().date())

    __table_args__ = (db.UniqueConstraint('userId', 'dietPlanId', name='unique_user_diet'),)
