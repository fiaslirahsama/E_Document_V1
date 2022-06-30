# from app_edoc.pemrograman.autentikasi import bp_autentikasi, controller_autentikasi, model_autentikasi
from app_edoc.pemrograman.dokumen import bp_dokumen, controller_dokumen, model_dokumen
from app_edoc.pemrograman.autentikasi.model_autentikasi import User, UserVariables
from app_edoc.pemrograman.dokumen.model_dokumen import File, Folder
from flask import render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db, BASEDIR, UPLOAD_FOLDER
from flask_login import login_user, login_required, current_user, logout_user
# from app_edoc.pemrograman.autentikasi.model_autentikasi import User
# roles = controller_autentikasi.roles()
import os
import subprocess
from os.path import join, dirname, realpath
from app_edoc import db
# BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(realpath(__file__)))))
# UPLOAD_FOLDER = os.path.join(BASEDIR, './static/files')
cekroot = BASEDIR + '\\static\\files'

def get_roles():
    roles = str(current_user.roles)
    if roles == 'RoleEnum.superadmin':
        roles = 'superadmin'
    elif roles == 'RoleEnum.manager':
        roles = 'manager'
    elif roles == 'RoleEnum.user':
        roles = 'user'
    return roles

def get_root_folder():
  rf = os.path.join(BASEDIR, UPLOAD_FOLDER) 
  os.chdir(rf)
  rf = os.getcwd()
  return rf

def get_cwd():
    cwd = db.session.query(UserVariables.current_working_directory).filter(UserVariables.userid == current_user.id, UserVariables.username == current_user.username).first()
    db.session.close()
    for row in cwd:
        current_working_directory = str(row)
    return current_working_directory

def get_root():
    rt = db.session.query(UserVariables.root).filter(UserVariables.userid == current_user.id, UserVariables.username == current_user.username).first()
    db.session.close()
    for row in rt:
        root = row
    return root

def update_data(current_working_directory, root):
    updateData = UserVariables.query.filter_by(userid = current_user.id, username = current_user.username).first()
    updateData.current_working_directory = current_working_directory
    updateData.root = root
    db.session.commit()
    db.session.close()

def get_departemen():
    dept = db.session.query(User.departemen).filter(User.id == current_user.id, User.username == current_user.username).first()
    for row in dept:
        departemen = row
    return departemen

@bp_dokumen.route('/dokumenmenu')
@login_required
def menu_dokumen():
    db.session.close()
    root = True
    current_working_directory = get_root_folder()
    update_data(current_working_directory, root)
    return render_template('dokumen/menu.html')

@bp_dokumen.route('/masterdokumenkontrol', methods=['GET', 'POST'])
@login_required
def master_dokumen():
    # if roles == 'user':
    #     return '404'
    # else:    
    #     return render_template('dokumen/master_dokumen.html')
    return render_template('dokumen/master_dokumen.html')

@bp_dokumen.route('/distribusidokumen', methods=['GET', 'POST'])
@login_required
def distribusi_dokumen():
    current_working_directory = get_cwd()
    root = get_root()
    print(current_working_directory)
    os.chdir(current_working_directory)
    roles = get_roles()
    if roles == 'superadmin' or roles == 'manager':
        file_list_query = db.session.query(File.file_name.label('name'), File.revision, File.file_size, File.file_ext, File.type.label('type')).filter(File.parent_path==current_working_directory)
        folder_list_query = db.session.query(Folder.folder_name.label('name'), db.null(), db.null(), Folder.folder_ext, Folder.type.label('type')).filter(Folder.parent_path==current_working_directory)
        file_list = file_list_query.union(folder_list_query).order_by('name').all()
        db.session.close()
    else:
        departemen = get_departemen()
        file_list_query = db.session.query(File.file_name.label('name'), File.revision, File.file_size, File.file_ext, File.type.label('type')).filter(File.parent_path==current_working_directory, (File.permission==departemen) | (File.permission=='all'))
        folder_list_query = db.session.query(Folder.folder_name.label('name'), db.null(), db.null(), Folder.folder_ext, Folder.type.label('type')).filter(Folder.parent_path==current_working_directory, (Folder.permission==departemen) | (Folder.permission=='all'))
        file_list = file_list_query.union(folder_list_query).order_by('name').all()
        db.session.close()
    # file_list = db.session.query(view_dir).all()
    
    # file_list_input = subprocess.check_output('dir', shell=True).decode('utf-8').split('\n')
    # file_list = []
    # for item in file_list_input[7:-3]:
    #     item_split = str(item).split()
    #     file_list.insert(len(file_list),item_split[-1])
    return render_template('dokumen/distribusi_dokumen.html', current_working_directory = current_working_directory, file_list = file_list, root=root)

@bp_dokumen.route('/createfolder', methods=['GET', 'POST'])
@login_required
def create_folder():
    # if request.method == 'POST':
    #     nama_folder = request.form['namafolder']
    #     permission = request.form['permission']
    #     folder_path = os.path.join(current_working_directory, nama_folder)
    #     os.makedirs(folder_path)
    #     # print(BASEDIR)
    #     # print(UPLOAD_FOLDER)
    #     print(nama_folder)
    controller_dokumen.createFolder()
    return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/createfile', methods=['GET', 'POST'])
@login_required
def create_file():
    controller_dokumen.createFile()
    return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/level_up', methods=['GET', 'POST'])
def level_up():
    # print(os.getcwd())
    current_working_directory = get_cwd()
    os.chdir(current_working_directory)
    # print(os.getcwd())
    # print(cekroot1, cekroot2)
    os.chdir('..')
    # print(os.getcwd())
    current_working_directory = os.getcwd()
    if cekroot == current_working_directory:
        root = True
        update_data(current_working_directory, root)
        return redirect(url_for('dokumen.distribusi_dokumen'))
    # print(current_working_directory)
    else:
        root = False
        update_data(current_working_directory, root)
        return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/level_down/<item>', methods=['GET', 'POST'])
def level_down(item):
    current_working_directory = get_cwd()
    root = False
    # print(os.getcwd())
    os.chdir(current_working_directory)
    # print(os.getcwd())
    next_directory = current_working_directory + '/' + item
    os.chdir(next_directory)
    # print(os.getcwd())
    current_working_directory = next_directory
    update_data(current_working_directory, root)
    # print(current_working_directory)
    return redirect(url_for('dokumen.distribusi_dokumen'))
    
@bp_dokumen.route('/open_file/<item>', methods=['GET', 'POST'])
def open_file(item):
    print(item)
    filename = str(item)
    return render_template('dokumen/open_file.html', filename=filename)

@bp_dokumen.route('/delete_folder/<item>', methods=['GET', 'POST'])
def delete_folder(item):
    return 'p'
@bp_dokumen.route('/delete_file/<item>', methods=['GET', 'POST'])
def delete_file(item):
    return 'q'