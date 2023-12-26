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
username = "postgres"
password = "Josiah1!"
host = "localhost"
port = "25060"
database = "django"
sslmode = "require"

# URL-encode the password
encoded_password = quote_plus(password)

# Construct the database URL with the encoded password and the new credentials
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}?sslmode={sslmode}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
