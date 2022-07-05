from flask import Blueprint

bp_dokumen = Blueprint('dokumen', __name__, static_folder='static', template_folder='templates')

from app_edoc.dcc.dokumen import view_dokumen