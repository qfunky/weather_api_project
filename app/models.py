from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, metadata

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

# Модель города
class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# Промежуточная таблица для связи многие ко многим (пользователи и города)
user_city = Table(
    "user_city",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("city_id", Integer, ForeignKey("cities.id"), primary_key=True)
)

# Связь с пользователями (многие ко многим)
users = relationship("User", secondary=user_city, back_populates="cities")
 # Связь с городами (многие ко многим)
cities = relationship("City", secondary=user_city, back_populates="users")