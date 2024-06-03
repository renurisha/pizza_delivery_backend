from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DB_URL='postgresql://postgres:postgres@localhost:5433/pizzadb'
engine=create_engine(DB_URL)
SessionLocal=sessionmaker(bind=engine)
# SessionLocal=sessionmaker()
Base=declarative_base()