from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.user import Base

engine = create_engine('sqlite:///users.db')  # Local SQLite DB file
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session() 