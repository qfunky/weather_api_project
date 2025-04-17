from databases import Database
from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
# Подключение к базе через библиотеку `databases`
database = Database(DATABASE_URL)
# Метаданные для описания таблиц
metadata = MetaData()
# Движок SQLAlchemy нужен только для создания таблиц
engine = create_engine(DATABASE_URL)