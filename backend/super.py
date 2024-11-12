from sqlalchemy.orm import sessionmaker
from your_models import UserDB, engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

superuser = UserDB(
    username="ArtShocheck",
    email="artshocheck@example.com",
    hashed_password=pwd_context.hash("sohack1"),
    is_superuser=True
)
db.add(superuser)
db.commit()
db.close()