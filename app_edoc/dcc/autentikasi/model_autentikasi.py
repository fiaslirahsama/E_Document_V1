from app_edoc import db
import enum
import os
from sqlalchemy import Enum
from flask import abort
from flask_login import UserMixin, current_user
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app_edoc import db, BASEDIR, UPLOAD_FOLDER_DCC, UPLOAD_FOLDER_METRO

### HELPER FUNCTION ###
def rootFolderDcc():
  rfd = os.path.join(BASEDIR, UPLOAD_FOLDER_DCC) 
  os.chdir(rfd)
  rfd = os.getcwd()
  return rfd

def rootFolderMetro():
  rfm = os.path.join(BASEDIR, UPLOAD_FOLDER_METRO)
  os.chdir(rfm)
  rfm = os.getcwd()
  return rfm

### MAIN FUNCTION ###
class UserVariables(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
  userid = db.Column(db.Integer, nullable = False)
  username = db.Column(db.String(30), nullable = False)
  current_working_directory_dcc = db.Column(db.String(9999), nullable = False, default=rootFolderDcc)
  current_working_directory_metro = db.Column(db.String(9999), nullable = False, default=rootFolderMetro)
  root_dcc = db.Column(db.Boolean, default=True)
  root_metro = db.Column(db.Boolean, default=True)

class RoleEnum(enum.Enum):
  user = 'user'
  managerdcc = 'managerdcc'
  managermetro = 'managermetro'
  superadmin = 'superadmin'

class User(db.Model, UserMixin ):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
  username = db.Column(db.String(30), nullable = False)
  nama = db.Column(db.String(50), nullable = False)
  password = db.Column(db.String(80), nullable = False)
  departemen = db.Column(db.String(80), nullable = False) #membedakan view per departemen
  roles = db.Column(Enum(RoleEnum), nullable = False, default=RoleEnum.user)
  
  def __repr__(self):
    return '<User {}>'.format(self.id) 
  def get_id(self):
    return (self.id)

class Controller(ModelView):
  def is_accessible(self):
    if current_user.roles == RoleEnum.superadmin:
      return current_user.is_authenticated
    else:
      return abort(404)
    # return current_user.is_authenticated
  def not_auth(self):
    return 'Maaf Anda tidak Punya Akses untuk melihat ini !!!'
  
class DashboardView(AdminIndexView):

    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    # @expose('/')
    # def index(self):

    #     return self.render(
    #         'admin/dashboard.html',
    #     )

  

  
  