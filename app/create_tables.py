from database import Base, engine
import models  # importa todos tus modelos para que SQLAlchemy los registre
from .models import Recordatorio

Base.metadata.create_all(bind=engine)
print("Tablas creadas")
