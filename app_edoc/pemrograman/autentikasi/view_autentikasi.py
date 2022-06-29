from app_edoc.pemrograman.autentikasi import bp_autentikasi, controller_autentikasi, model_autentikasi
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_edoc import db
from flask_login import login_user, login_required, current_user, logout_user
from app_edoc.pemrograman.autentikasi.model_autentikasi import User

@bp_autentikasi.route('/')
def index():
    return redirect(url_for('autentikasi.login'))

@bp_autentikasi.route('/login', methods=['GET', 'POST'])
def login():
    render_self, message = controller_autentikasi.login()
    if not render_self:
        return redirect(url_for('autentikasi.home'))
    return render_template('autentikasi/login.html', message = message)

@bp_autentikasi.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('autentikasi.index'))

@bp_autentikasi.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # roles = controller_autentikasi.home()
    return render_template('home.html')

@bp_autentikasi.route('/tes', methods=['GET', 'POST'])
@login_required
def tes():
    # roles = controller_autentikasi.home()
    return 'tes'