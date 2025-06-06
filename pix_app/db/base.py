from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

DATABASE_URL = "sqlite:///pix_app/data/database.db"

mapper_registry = registry()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database():
    """Inicializa o banco"""
    mapper_registry.metadata.create_all(bind=engine)
