import os
import pymysql
from os.path import join, dirname, realpath
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database

# set the base directory
BASEDIR = os.path.abspath(os.path.dirname(realpath(__file__)))

#
def validateDatabase(DATABASE_FILE):
    dbName = str(os.environ.get("DB_NAME"))
    dbFile = DATABASE_FILE
    engine = create_engine(dbFile)
    if not database_exists(engine.url): # Checks for the first time  
        create_database(engine.url)     # Create new DB    
        print(str(dbName)+" Database Created") # Verifies if database is there or not.
    else:
        print("Database "+str(dbName)+" Running")

#
def createFolder(PATH):
    folderPath = os.path.join(BASEDIR, PATH)
    os.makedirs(folderPath)

# Create the super class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FOLDER_FILES = os.environ.get('FOLDER_FILES')
    CEK_FOLDER_FILES = os.path.exists(FOLDER_FILES)
    if not CEK_FOLDER_FILES:
        createFolder(FOLDER_FILES)
        print('Folder Telah Dibuat')

  # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  # SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  
# Create the development config
class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql:///'+os.path.join(basedir, 'coba_db.db') #TODO
    UPLOAD_FOLDER = os.path.join(BASEDIR, './app_edoc/static/files')


    DB_HOST = str(os.environ.get("DB_HOST"))
    DB_NAME = str(os.environ.get("DB_NAME"))
    DB_USERNAME = str(os.environ.get("DB_USERNAME"))
    DB_PASSWORD = str(os.environ.get("DB_PASSWORD"))

    DATABASE_FILE = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME
    validateDatabase(DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = DATABASE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True 

  # secret_key_mysql = 'inipassword' # untuk proteksi extra

  # host_mysql = ['MYSQL_HOST']='192.168.5.171'  # dikoneksikan dengan database
  # username_mysql = ['MYSQL_USER']='admin'
  # password_mysql = ['MYSQL_PASSWORD']='666666'
  # database_mysql = ['MYSQL_DB']='ubs_univ'




  
  
  
  
  

  
  
