from databases import Database
from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

database = Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL)