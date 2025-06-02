# aturmation_app/models/user.py
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from .meta import Base
from passlib.context import CryptContext
import enum

class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.staff)
    photo = Column(String(255), nullable=True) # Opsional, bisa dihapus jika ingin lebih sederhana

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "photo": self.photo
        }