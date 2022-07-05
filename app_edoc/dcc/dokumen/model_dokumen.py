from datetime import datetime
from app_edoc import db

### HELPER FUNCTION ###
def waktu_sekarang():
    now = datetime.now()
    return now

### MAIN FUNCTION ###

# Create File Dcc
class FileDcc(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
  file_id = db.Column(db.String(99), nullable = False)
  file_name = db.Column(db.String(99), nullable = False)
  revision = db.Column(db.String(99), nullable = False)
  file_size = db.Column(db.String(30), nullable = False)
  file_ext = db.Column(db.String(10), nullable = False)
  permission = db.Column(db.String(999), nullable = False)
  parent_path = db.Column(db.String(99), nullable = False)
  type = db.Column(db.String(99), nullable = False, default='file')
  created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
  created_by = db.Column(db.String(30), nullable=False)
  updated_at = db.Column(db.DateTime)
  updated_by = db.Column(db.String(30))
  update_no = db.Column(db.Integer, default=1, nullable=False)
  flag = db.Column(db.Boolean, nullable=False, default=True)
  status = db.Column(db.String(99), nullable=False, default='ACTIVE')

#Create Dcc Folder Table
class FolderDcc(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
  folder_id = db.Column(db.String(99), nullable = False)
  folder_name = db.Column(db.String(99), nullable = False)
  folder_ext = db.Column(db.String(20), nullable = False, default='directory')
  permission = db.Column(db.String(999), nullable = False, default='all')
  parent_path = db.Column(db.String(99), nullable = False)
  type = db.Column(db.String(99), nullable = False, default='folder')
  created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
  created_by = db.Column(db.String(30), nullable=False)
  updated_at = db.Column(db.DateTime)
  updated_by = db.Column(db.String(30))
  update_no = db.Column(db.Integer, default=1, nullable=False)
  flag = db.Column(db.Boolean, nullable=False, default=True)
  status = db.Column(db.String(99), nullable=False, default='ACTIVE')