from sqlalchemy import create_engine

from logistics_ml.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
