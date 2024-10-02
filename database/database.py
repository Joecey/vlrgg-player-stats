from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

SQLALCHEMY_DATABASE_URL = os.environ.get("POSTGRES_URL")

# create SQLAlchemy engine which will be used to power ORM
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal which will then be turned into a Database session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this Base class will be inherited by database models and classes (ORM models)
Base = declarative_base()