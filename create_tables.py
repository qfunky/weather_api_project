from app.database import engine, metadata
from app import models  # нужно, чтобы зарегистрировать таблицу в metadata

metadata.create_all(engine)

print("Таблицы созданы!")