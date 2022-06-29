from flask import Blueprint

bp_autentikasi = Blueprint('autentikasi', __name__, static_folder='static', template_folder='templates')

from app_edoc.pemrograman.autentikasi import view_autentikasi