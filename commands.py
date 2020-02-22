   # Dependencies
    # ----------------------------------
    # Imports the method used for connecting to DBs
from sqlalchemy import create_engine
from config import DATABASE_URL
 
def create_tables():

  engine = create_engine(DATABASE_URL)
  engine.execute('CREATE TABLE public."GeoTagData" (    index integer,    "FileAddress" text ,   "ImageTimeStamp" text ,  city text , country text,  county text ,    landmark ,    latitude real,    longitude real,    state text ,    zipcode integer)')

