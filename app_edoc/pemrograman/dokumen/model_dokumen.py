from datetime import datetime, timedelta
from app_edoc import db
from flask_sqlalchemy import SQLAlchemy

def waktu_sekarang():
    now = datetime.now()
    return now

class Document(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  file_path = db.Column(db.String(99), nullable = False)
  file_name = db.Column(db.String(99), nullable = False)
  file_size = db.Column(db.String(30), nullable = False)
  file_ext = db.Column(db.String(10), nullable = False)
  revision = db.Column(db.String(99), nullable = False)
  permission = db.Column(db.String(99), nullable = False)
  created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
  created_by = db.Column(db.String(30), nullable=False)
  updated_at = db.Column(db.DateTime)
  updated_by = db.Column(db.String(30))
  update_no = db.Column(db.Integer, default=1)
  flag = db.Column(db.String(10), nullable=False, default='on')

class Folder(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  pathname = db.Column(db.String(99), nullable = False)
  permission = db.Column(db.String(99))
  created_at = db.Column(db.DateTime, nullable=False, default=waktu_sekarang)
  created_by = db.Column(db.String(30), nullable=False)
  updated_at = db.Column(db.DateTime)
  updated_by = db.Column(db.String(30))
  flag = db.Column(db.String(10), nullable=False, default='on')
# class RoleEnum(enum.Enum):
#   user = 'user'
#   manager = 'manager'
#   superadmin = 'superadmin'

# class User(db.Model, UserMixin ):
#   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#   username = db.Column(db.String(30), nullable = False)
#   nama = db.Column(db.String(50), nullable = False)
#   password = db.Column(db.String(80), nullable = False)
#   departemen = db.Column(db.String(80), nullable = False) #membedakan view per departemen
#   roles = db.Column(Enum(RoleEnum), nullable = False)
#   # is_user = db.Column(db.Boolean, default=False)
#   # is_manager = db.Column(db.Boolean, default=False)
#   # is_admin = db.Column(db.Boolean, default=False)
  
#   def __repr__(self):
#     return '<User {}>'.format(self.id) 
#   def get_id(self):
#     return (self.id)

# class Controller(ModelView):
#   def is_accessible(self):
#     if current_user.roles == RoleEnum.superadmin:
#       return current_user.is_authenticated
#     else:
#       return abort(404)
#     # return current_user.is_authenticated
#   def not_auth(self):
#     return 'Maaf Anda tidak Punya Akses untuk melihat ini !!!'
  
# class DashboardView(AdminIndexView):

#     def is_visible(self):
#         # This view won't appear in the menu structure
#         return False

#     # @expose('/')
#     # def index(self):

#     #     return self.render(
#     #         'admin/dashboard.html',
#     #     )

  

  
  