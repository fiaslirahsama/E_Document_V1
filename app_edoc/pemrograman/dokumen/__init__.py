from flask import Blueprint

bp_dokumen = Blueprint('dokumen', __name__, static_folder='static', template_folder='templates')

from app_edoc.pemrograman.dokumen import view_dokumen