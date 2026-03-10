from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Création du moteur de connexion
# pool_pre_ping=True permet de vérifier que la connexion est vivante avant de l'utiliser
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 2. Création de l'usine à sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Classe de base pour nos modèles (Entities)
Base = declarative_base()

# 4. Dépendance pour FastAPI
# Cette fonction sera injectée dans les routes pour récupérer une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()