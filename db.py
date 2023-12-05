from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



from urllib.parse import quote_plus

# Original password
raw_password = "Cr!st0V!v3J3susS@lvA2023!"

# URL-encode the password
encoded_password = quote_plus(raw_password)

# Construct the database URL with the encoded password
SQLALCHEMY_DATABASE_URL = f"postgresql://gpstracker2:{encoded_password}@localhost/raw_data_db"



# SQLALCHEMY_DATABASE_URL = "postgresql://gpstracker2:Cr!st0V!v3J3susS@lvA2023!@localhost/raw_data_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
