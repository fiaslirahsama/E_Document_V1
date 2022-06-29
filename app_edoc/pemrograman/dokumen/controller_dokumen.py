from app_edoc.pemrograman.dokumen import bp_dokumen, view_dokumen, model_dokumen
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db
from flask_login import login_user, login_required, current_user, logout_user
from os.path import join, dirname, realpath
import os
from werkzeug.utils import secure_filename
# from app_edoc.pemrograman.autentikasi.model_autentikasi import User

def createFolder():
    if request.method == 'POST':
        namafolder = request.form['namafolder']
        permission = request.form['permission']
        
        # print(BASEDIR)
        # print(UPLOAD_FOLDER)
        print(namafolder)
        # createdFolder = os.path.join(UPLOAD_FOLDER, namafolder)
        # print(createdFolder)

def createFile():
    if request.method == 'POST':
        file = request.files['file']
        revision = request.form['revision']
        permission = request.form['permission']
        created_by = current_user.nama

        if not permission:
            permission = 'all'

        if file:
            files = secure_filename(file.filename)
            filesplit = files.split('.')
            fileext = filesplit[-1]
            filefolder = os.path.join(UPLOAD_FOLDER, files)
            file.save(filefolder)
            size = os.stat(filefolder).st_size
            lensize = len(str(size))
            if lensize >= 7:
                size = size/(1024*1024)
                size = float("{0:.2f}".format(size))
                size = str(size)+' MB'
            elif lensize >=4 and lensize < 7:
                size = size/1024
                size = float("{0:.2f}".format(size))
                size = str(size)+' KB'
            else:
                size = str(size)+' B'
            print(files,filefolder, fileext, size, lensize)
            flash('uploaded')
        else:
            flash('Silahkan pilih file yang mau diupload')



# def menuDokumen():
# def login():
#     message = ''
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()

#         if not user:
#             message = 'Username salah / tidak terdaftar, silahkan coba lagi'
#         elif user.password != password:
#             message = 'Password salah, silahkan coba lagi.'

#         if not message:
#             renderSelf = False
#             login_user(user)
#             db.session.close()
#             return renderSelf, message
#         else:
#             renderSelf = True
#             return renderSelf, message
#     else:
#         renderSelf = True
#         return renderSelf, message

# def home():
#     role = db.session.query(User.roles).filter(User.id == current_user.id).first()
#     for roles in role:
#         roles = str(roles)
#         if roles == 'RoleEnum.superadmin':
#             roles = 'superadmin'
#             return roles
#         elif roles == 'RoleEnum.manager':
#             roles = 'manager'
#             return roles
#         elif roles == 'RoleEnum.user':
#             roles = 'user'
#             return roles