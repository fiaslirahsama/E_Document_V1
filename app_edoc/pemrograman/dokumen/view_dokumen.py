# from app_edoc.pemrograman.autentikasi import bp_autentikasi, controller_autentikasi, model_autentikasi
from app_edoc.pemrograman.dokumen import bp_dokumen, controller_dokumen, model_dokumen
from app_edoc.pemrograman.autentikasi import controller_autentikasi
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db
from flask_login import login_user, login_required, current_user, logout_user
# from app_edoc.pemrograman.autentikasi.model_autentikasi import User
# roles = controller_autentikasi.roles()
import os
import subprocess
from os.path import join, dirname, realpath
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(realpath(__file__)))))
UPLOAD_FOLDER = os.path.join(BASEDIR, './static/files')

@bp_dokumen.route('/dokumenmenu')
@login_required
def menu_dokumen():
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
    current_working_directory = os.path.join(BASEDIR, UPLOAD_FOLDER)
    os.chdir(current_working_directory)
    file_list = subprocess.check_output('dir', shell=True).decode('utf-8').split('\n')
    return render_template('dokumen/distribusi_dokumen.html', current_working_directory = current_working_directory, file_list = file_list)

@bp_dokumen.route('/createfolder', methods=['GET', 'POST'])
@login_required
def create_folder():
    controller_dokumen.createFolder()
    return redirect(url_for('dokumen.distribusi_dokumen'))

@bp_dokumen.route('/createfile', methods=['GET', 'POST'])
@login_required
def create_file():
    controller_dokumen.createFile()
    return redirect(url_for('dokumen.distribusi_dokumen'))