from app_edoc.dcc.dokumen import bp_dokumen, controller_dokumen
from flask import render_template, redirect, url_for, abort
from flask_login import login_user, login_required, current_user
import os

### HELPER FUNCTION ###
#
def get_roles():
    roles = str(current_user.roles)
    if roles == 'RoleEnum.superadmin':
        roles = 'superadmin'
    elif roles == 'RoleEnum.managerdcc':
        roles = 'managerdcc'
    elif roles == 'RoleEnum.managermetro':
        roles = 'managermetro'
    elif roles == 'RoleEnum.user':
        roles = 'user'
    return roles
### MAIN FUNCTION ###
#
@bp_dokumen.route('/dokumenmenu')
@login_required
def menu_dokumen():
    controller_dokumen.menuDokumen()
    return render_template('dokumen/menu.html')

#
@bp_dokumen.route('/masterdokumenkontrol', methods=['GET', 'POST'])
@login_required
def master_dokumen():
    roles = get_roles()
    if roles == 'user' or roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.masterDokumen()
        return render_template('dokumen/master_dokumen.html')

#
@bp_dokumen.route('/distribusidokumen', methods=['GET', 'POST'])
@login_required
def distribusi_dokumen():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        cwd_dcc, file_list, root, option_departemen= controller_dokumen.distribusiDokumen()
        return render_template('dokumen/distribusi_dokumen.html', 
                current_working_directory = cwd_dcc, 
                file_list = file_list, 
                root=root, 
                option_departemen=option_departemen
                )

#
@bp_dokumen.route('/createfolderdcc', methods=['GET', 'POST'])
@login_required
def create_folder_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.createFolderDcc()
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
@bp_dokumen.route('/createfiledcc', methods=['GET', 'POST'])
@login_required
def create_file_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.createFileDcc()
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
@bp_dokumen.route('/backdirectorydcc', methods=['GET', 'POST'])
@login_required
def back_directory_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.backDirectoryDcc()
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
@bp_dokumen.route('/nextdirectorydcc/<item>', methods=['GET', 'POST'])
@login_required
def next_directory_dcc(item):
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.nextDirectoryDcc(item)
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
@bp_dokumen.route('/openfiledcc/<item>', methods=['GET', 'POST'])
def open_file_dcc(item):
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        file_name, file_path= controller_dokumen.openFileDcc(item)
        return render_template('dokumen/open_file_pdf.html', filename=file_name, filepath=file_path)

#
bp_dokumen.route('/fetchdatafolderdcc', methods=['GET', 'POST'])
def fetch_data_folder_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        id, folder_id, folder_name, current_working_directory, permission_departemen, option_departemen, permission_departemen, current_working_directory = controller_dokumen.fetchDataFolderDcc()
        return render_template('dokumen/edit_folder.html',
                                id = id,
                                folder_id = folder_id, 
                                folder_name_value=folder_name, 
                                option_departemen=option_departemen,
                                permission_departemen = permission_departemen,
                                current_working_directory = current_working_directory
                                )

#
@bp_dokumen.route('/updatefolderdcc', methods=['GET', 'POST'])
def update_folder_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.updateFolderDcc()
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
@bp_dokumen.route('/fetchdatafiledcc', methods=['GET', 'POST'])
def fetch_data_file_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        id, file_id, file_name, current_working_directory, permission_departemen, option_departemen = controller_dokumen.fetchDataFileDcc()
        return render_template('dokumen/edit_file.html',
                                id = id,
                                file_id = file_id,
                                file_name = file_name,
                                current_working_directory = current_working_directory,
                                permission_departemen = permission_departemen,
                                option_departemen = option_departemen
                                )

#
@bp_dokumen.route('/updatefiledcc', methods=['GET', 'POST'])
def update_file_dcc():
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.updateFileDcc()
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
bp_dokumen.route('/deletefolderdcc/<id>,<folder_id>,<folder_name>', methods=['GET','POST'])
def delete_folder_dcc(id, folder_id, folder_name):
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.deleteFolderDcc(id, folder_id, folder_name)
        return redirect(url_for('dokumen.distribusi_dokumen'))

#
bp_dokumen.route('/deletefiledcc/<id>,<file_id>,<file_name>', methods=['GET','POST'])
def delete_file_dcc(id, file_id, file_name):
    roles = get_roles()
    if roles == 'managermetro':
        return abort(404)
    else:
        controller_dokumen.deleteFileDcc(id, file_id, file_name)
        return redirect(url_for('dokumen.distribusi_dokumen'))