from app_edoc import db
import enum
from sqlalchemy import Enum
from flask import abort
from flask_login import UserMixin, current_user
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView 

class RoleEnum(enum.Enum):
  user = 'user'
  manager = 'manager'
  superadmin = 'superadmin'

class User(db.Model, UserMixin ):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(30), nullable = False)
  nama = db.Column(db.String(50), nullable = False)
  password = db.Column(db.String(80), nullable = False)
  departemen = db.Column(db.String(80), nullable = False) #membedakan view per departemen
  roles = db.Column(Enum(RoleEnum), nullable = False)
  # is_user = db.Column(db.Boolean, default=False)
  # is_manager = db.Column(db.Boolean, default=False)
  # is_admin = db.Column(db.Boolean, default=False)
  
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

  

  
  