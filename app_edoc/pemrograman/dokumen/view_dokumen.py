# from app_edoc.pemrograman.autentikasi import bp_autentikasi, controller_autentikasi, model_autentikasi
from app_edoc.pemrograman.dokumen import bp_dokumen, controller_dokumen, model_dokumen
from app_edoc.pemrograman.autentikasi import controller_autentikasi
from flask import render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db, BASEDIR, UPLOAD_FOLDER
from flask_login import login_user, login_required, current_user, logout_user
# from app_edoc.pemrograman.autentikasi.model_autentikasi import User
# roles = controller_autentikasi.roles()
import os
import subprocess
from os.path import join, dirname, realpath
# BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(realpath(__file__)))))
# UPLOAD_FOLDER = os.path.join(BASEDIR, './static/files')
cekroot1 = current_working_directory = os.path.join(BASEDIR, UPLOAD_FOLDER)
cekroot2 = BASEDIR + '\\static\\files'
root = True

@bp_dokumen.route('/dokumenmenu')
@login_required
def menu_dokumen():
    global current_working_directory, root
    root = True
    current_working_directory = os.path.join(BASEDIR, UPLOAD_FOLDER)
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
    print(current_working_directory)
    os.chdir(current_working_directory)
    file_list_input = subprocess.check_output('dir', shell=True).decode('utf-8').split('\n')
    file_list = []
    for item in file_list_input[7:-3]:
        item_split = str(item).split()
        file_list.insert(len(file_list),item_split[-1])
    return render_template('dokumen/distribusi_dokumen.html', current_working_directory = current_working_directory, file_list = file_list, root=root)

@bp_dokumen.route('/createfolder', methods=['GET', 'POST'])
@login_required
def create_folder():
    if request.method == 'POST':
        nama_folder = request.form['namafolder']
        permission = request.form['permission']
        folder_path = os.path.join(current_working_directory, nama_folder)
        os.makedirs(folder_path)
        # print(BASEDIR)
        # print(UPLOAD_FOLDER)
        print(nama_folder)
        return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/createfile', methods=['GET', 'POST'])
@login_required
def create_file():
    controller_dokumen.createFile()
    return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/level_up', methods=['GET', 'POST'])
def level_up():
    global current_working_directory, root
    # print(os.getcwd())
    os.chdir(current_working_directory)
    # print(os.getcwd())
    # print(cekroot1, cekroot2)
    os.chdir('..')
    # print(os.getcwd())
    current_working_directory = os.getcwd()
    if cekroot1 == current_working_directory or cekroot2 == current_working_directory:
        root = True
        return redirect(url_for('dokumen.distribusi_dokumen'))
    # print(current_working_directory)
    else:
        root = False
        return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/level_down/<item>', methods=['GET', 'POST'])
def level_down(item):
    global current_working_directory, root
    root = False
    # print(os.getcwd())
    os.chdir(current_working_directory)
    # print(os.getcwd())
    next_directory = current_working_directory + '/' + item
    os.chdir(next_directory)
    # print(os.getcwd())
    current_working_directory = next_directory
    # print(current_working_directory)
    return redirect(url_for('dokumen.distribusi_dokumen'))
    
@bp_dokumen.route('/open_file/<item>', methods=['GET', 'POST'])
def open_file(item):
    print(item)
    filename = str(item)
    return render_template('dokumen/open_file.html', filename=filename)