# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = "postgresql+psycopg2://postgres:!2000@localhost/blogdb"

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()




import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Safely encode the password containing the '!' character
encoded_password = urllib.parse.quote_plus("!2000")

# 2. Inject the encoded variable into your connection string
DATABASE_URL = f"postgresql+psycopg2://postgres:{encoded_password}@localhost/blogdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
