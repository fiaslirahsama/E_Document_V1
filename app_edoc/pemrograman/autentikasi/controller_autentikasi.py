from app_edoc.pemrograman.autentikasi import bp_autentikasi, view_autentikasi, model_autentikasi
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db
from flask_login import login_user, login_required, current_user, logout_user
from app_edoc.pemrograman.autentikasi.model_autentikasi import User, UserVariables

def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user:
            message = 'Username salah / tidak terdaftar, silahkan coba lagi'
        elif user.password != password:
            message = 'Password salah, silahkan coba lagi.'

        if not message:
            renderSelf = False
            login_user(user)
            cekData = UserVariables.query.filter_by(userid = current_user.id, username=current_user.username).first()
            if cekData:
                cekData.current_working_directory = model_autentikasi.rootFolder()
                cekData.root = True
                db.session.commit()
                db.session.close()
                return renderSelf, message
            else:
                insertData = UserVariables(userid = current_user.id, username=current_user.username)
                db.session.add(insertData)
                db.session.commit()
                db.session.close()
                return renderSelf, message
        else:
            renderSelf = True
            return renderSelf, message
    else:
        renderSelf = True
        return renderSelf, message

# def roles():
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