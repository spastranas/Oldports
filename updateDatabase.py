def UpdateDB(NewFile):

    # Dependencies
    # ----------------------------------
    # Imports the method used for connecting to DBs
    from sqlalchemy import create_engine
    # Imports the methods needed to abstract classes into tables
    from sqlalchemy.ext.declarative import declarative_base
    # Allow us to declare column types
    from sqlalchemy import Column, Integer, String, Float 


    # Create Class
    # ----------------------------------
    Base = declarative_base()
    class UploadClass(Base):
        __tablename__ = 'GeoTagData'
        __table_args__ = { 'extend_existing': True }

        index=Column (Integer,primary_key=True)
        latitude= Column (Float)
        longitude= Column (Float)
        landmark=Column(String(255))
        country=Column(String(255))
        state=Column(String(255))
        county=Column(String(255))
        city=Column(String(255))
        zipcode=Column(Integer)
        ImageTimeStamp=Column(String(255))
        FileAddress=Column(String(255))
        

    # add the new picture data into a dataframe
    import ProcessPicture
    picAddress=NewFile
    # execute function into a variable
    df=ProcessPicture.ExtractPicData(picAddress)


    # Create variables to hold new picture data info
    FileAddress=df['FileAddress']
    ImageTimeStamp=df['ImageTimeStamp']
    city=df['city']
    country=df['country']
    county=df['county']
    landmark=df['landmark']
    latitude=df['latitude']
    longitude=df['longitude']
    state=df['state']
    zipcode=df['zipcode']

    # look for the last index, so we can add the index column
    # Create Database Connection
    # ----------------------------------
    database_path = "db/Oldports.sqlite"
    engine = create_engine(f"sqlite:///{database_path}")
    # conn = engine.connect()
    data = engine.execute("SELECT *  FROM GeoTagData")
    index=[]
    for record in data:
        index.append(record)
    # index int a variable
    index=len(index)

    # update the class with the dataframe varables
    pictureData=UploadClass(index=index,FileAddress=FileAddress,ImageTimeStamp=ImageTimeStamp, city=city, country=country,county=county, landmark=landmark, latitude=latitude, longitude=longitude,state=state,zipcode=zipcode) 

    # Create a "Metadata" Layer That Abstracts our SQL Database
    Base.metadata.create_all(engine)
    # Create a Session Object to Connect to DB
    # ----------------------------------
    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    # Add Records to the Appropriate DB
    # ----------------------------------
    session.add(pictureData)

    session.commit()

    ProcessPicture.make_thumbnail(NewFile)
