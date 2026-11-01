from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib

from .config import settings

password=urllib.parse.quote_plus(settings.DB_PASSWORD)

db_url=f"postgresql+psycopg2://{settings.DB_USERNAME}:{password}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"

engine=create_engine(db_url)

SessionLocal=sessionmaker(expire_on_commit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()