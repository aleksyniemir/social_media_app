from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


engine = create_engine(
    "postgresql://postgres:haslo123@localhost:5555/webowka_projekt_zaliczeniowy",
    echo=True, 
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)