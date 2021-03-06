import os
import pymysql
from os.path import join, dirname, realpath
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database

# set the base directory
BASEDIR = os.path.abspath(os.path.dirname(realpath(__file__)))

### HELPER FUNCTION ######
# CREATE DATABASE IF NOT EXIST
def validateDatabase(DATABASE_FILE):
    dbName = str(os.environ.get("DB_NAME"))
    dbFile = DATABASE_FILE
    engine = create_engine(dbFile)
    if not database_exists(engine.url): # Checks for the first time  
        create_database(engine.url)     # Create new DB    
        print(str(dbName)+" Database Created") # Verifies if database is there or not.
    else:
        print("Database "+str(dbName)+" Running")

# CREATE FOLDER IF NOT EXIST
def createFolder(PATH):
    folderPath = os.path.join(BASEDIR, PATH)
    os.makedirs(folderPath)

### MAIN FUNCTION ####
# Create the super class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FOLDER_FILES_DCC = os.environ.get('FOLDER_FILES_DCC')
    FOLDER_FILES_METRO = os.environ.get('FOLDER_FILES_METRO')
    CEK_FOLDER_FILES_DCC = os.path.exists(FOLDER_FILES_DCC)
    CEK_FOLDER_FILES_METRO = os.path.exists(FOLDER_FILES_METRO)
    if not CEK_FOLDER_FILES_DCC:
        createFolder(FOLDER_FILES_DCC)
        print('Folder E-Document Control Telah Dibuat')
    
    if not CEK_FOLDER_FILES_METRO:
        createFolder(FOLDER_FILES_METRO)
        print('Folder E-Metrologi Telah Dibuat')


  # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  # SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  
# Create the development config
class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql:///'+os.path.join(basedir, 'coba_db.db') #TODO

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




  
  
  
  
  

  
  
