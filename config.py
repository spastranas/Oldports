import os

S3_BUCKET                 = os.environ.get("S3_BUCKET")
S3_KEY                    = os.environ.get("AWS_ACCESS_KEY_ID")
S3_SECRET                 = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000

API_KEY                 =os.environ.get("API_KEY")

POSTGRES_URL  =os.environ.get("POSTGRES_URL")
POSTGRES_USER  =os.environ.get("POSTGRES_USER")
POSTGRES_PW  =os.environ.get("POSTGRES_PW")
POSTGRES_DB  =os.environ.get("POSTGRES_DB")
#DATABASE_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

#DATABASE_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=os.environ.get("POSTGRES_USER"),pw=os.environ.get("POSTGRES_PW"),url=os.environ.get("POSTGRES_URL"),db=os.environ.get("POSTGRES_DB"))
DATABASE_URL = '{user}:{pw}@{url}/{db}'.format(user=os.environ.get("POSTGRES_USER"),pw=os.environ.get("POSTGRES_PW"),url=os.environ.get("POSTGRES_URL"),db=os.environ.get("POSTGRES_DB"))

#SQLALCHEMY_DATABASE_URI = DATABASE_URL


