from app.database import engine, Base  # Импортируем engine и Base
from app import models  # Нужно, чтобы зарегистрировать таблицу в metadata

# Создаём все таблицы в базе данных
Base.metadata.create_all(engine)

print("Таблицы созданы!")