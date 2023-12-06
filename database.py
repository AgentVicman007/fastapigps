# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker



# from urllib.parse import quote_plus

# # Original password
# raw_password = "Cr!st0V!v3J3susS@lvA2023!"

# # URL-encode the password
# encoded_password = quote_plus(raw_password)

# # Construct the database URL with the encoded password
# SQLALCHEMY_DATABASE_URL = f"postgresql://gpstracker2:{encoded_password}@localhost/raw_data_db"



# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Prod 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# New database credentials
username = "db"
password = "AVNS_iyizor6NGyef7T-4fwI"
host = "app-8047bdcf-fa71-49a8-aa04-ac6abcd59948-do-user-10862778-0.c.db.ondigitalocean.com"
port = "25060"
database = "db"
sslmode = "require"

# URL-encode the password
encoded_password = quote_plus(password)

# Construct the database URL with the encoded password and the new credentials
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}?sslmode={sslmode}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
