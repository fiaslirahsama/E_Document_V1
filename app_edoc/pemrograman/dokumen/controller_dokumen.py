from app_edoc.pemrograman.dokumen import bp_dokumen, view_dokumen, model_dokumen
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db
from flask_login import login_user, login_required, current_user, logout_user
from os.path import join, dirname, realpath
import os
from werkzeug.utils import secure_filename
from app_edoc.pemrograman.dokumen.model_dokumen import File, Folder
# from app_edoc.pemrograman.autentikasi.model_autentikasi import User

def createFile():
    if request.method == 'POST':
        file = request.files['file']
        revision = request.form['revision']
        permission = request.form['permission']
        currentWorkingDirectory = request.form['cwd']

        if not permission:
            permission = 'all'

        if file:
            fileName = secure_filename(file.filename)
            fileSplit = fileName.split('.')
            fileExt = fileSplit[-1]
            filefolder = os.path.join(currentWorkingDirectory, fileName)
            file.save(filefolder)
            fileSize = os.stat(filefolder).st_size
            lensize = len(str(fileSize))
            if lensize >= 7:
                fileSize = fileSize/(1024*1024)
                fileSize = float("{0:.2f}".format(fileSize))
                fileSize = str(fileSize)+' MB'
            elif lensize >=4 and lensize < 7:
                fileSize = fileSize/1024
                fileSize = float("{0:.2f}".format(fileSize))
                fileSize = str(fileSize)+' KB'
            else:
                fileSize = str(fileSize)+' B'
            
            insertData = File(file_name=fileName, revision=revision, file_size=fileSize, file_ext=fileExt, permission = permission, parent_path = currentWorkingDirectory, created_by=current_user.nama)
            db.session.add(insertData)
            db.session.commit()
            db.session.close()
            # print(files,filefolder, fileext, size, lensize)
            flash('uploaded')
        else:
            flash('Silahkan pilih file yang mau diupload')

def createFolder():
    if request.method == 'POST':
        namaFolder = request.form['namafolder']
        permission = request.form['permission']
        if not permission:
            permission = 'all'
        currentWorkingDirectory= request.form['cwd']
        namaFolder = str(namaFolder)
        folder_path = os.path.join(currentWorkingDirectory, namaFolder)
        os.makedirs(folder_path)
        insertData = Folder(folder_name=namaFolder, permission = permission, parent_path = currentWorkingDirectory, created_by = current_user.nama)
        db.session.add(insertData)
        db.session.commit()
        db.session.close()
        # print(BASEDIR)
        # print(UPLOAD_FOLDER)
        print(folder_path)

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