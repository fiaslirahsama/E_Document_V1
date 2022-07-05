from asyncore import file_dispatcher
from msilib.schema import File
from app_edoc.dcc import autentikasi
from app_edoc.dcc.autentikasi import model_autentikasi
from app_edoc.dcc.autentikasi.model_autentikasi import User, UserVariables
from app_edoc.dcc.dokumen.model_dokumen import FileDcc, FolderDcc
from flask import request, flash
from app_edoc import db
from flask_login import current_user
from os.path import join, dirname
import os
from werkzeug.utils import secure_filename
from datetime import datetime

### HELPER FUNCTION ###
# Get Time Now
def waktuSekarang():
    now = datetime.now()
    return now
# Update Table Variable User
def updateVariableUser(cwdDcc, rootDcc):
    updateVariable = UserVariables.query.filter_by(userid = current_user.id, username = current_user.username).first()
    updateVariable.current_working_directory_dcc = cwdDcc
    updateVariable.root_dcc = rootDcc
    db.session.commit()
    db.session.close()
# Get roles variables
def getRoles():
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
#
def getOptionDepartemen():
    dept = db.session.query(User.departemen).distinct().all()
    db.session.close()
    return dept
#
def getRootVariable():
    urv = db.session.query(UserVariables.root_dcc).filter(UserVariables.userid == current_user.id, UserVariables.username == current_user.username).first()
    db.session.close()
    for row in urv:
        root = row
    return root
#
def getCwdDcc():
    cwdDcc = db.session.query(UserVariables.current_working_directory_dcc).filter(UserVariables.userid == current_user.id, UserVariables.username == current_user.username).first()
    db.session.close()
    for row in cwdDcc:
        cwd = str(row)
    return cwd
#
def getDepartemen():
    dept = db.session.query(User.departemen).filter(User)
    db.session.close()
    departemen = ''
    for row in dept:
        departemen += '('
        departemen += row
        departemen += ')'
    return departemen
#
def getPermission(permissionInput):
    permission=''
    for row in permissionInput:
        if not row:
            permission = '(all)'
        else:
            permission += '('
            permission += row
            permission += ')'
    return permission
#
def insertFolderDcc(namaFolder, permission, currentWorkingDirectory):
    folderId = 0
    cekFold = db.session.query(FolderDcc.folder_id).distinct().all()
    db.session.close()
    if not cekFold:
        folderId = 1
    else:
        folderId = len(cekFold) + 1
    insertData = FolderDcc(folder_id=folderId, folder_name=namaFolder, permission = permission, parent_path = currentWorkingDirectory, created_by = current_user.nama)
    db.session.add(insertData)
    db.session.commit()
    db.session.close()
    flash('Folder '+namaFolder+' berhasil dibuat')
#
def insertFileDcc(namaFile, revision, sizeFile, extFile, permission, currentWorkingDirectory):
    FileId = 0
    cekFile = db.session.query(FileDcc.file_id).distinct().all()
    db.session.close()
    if not cekFile:
        fileId = 1
    else:
        fileId = len(cekFile) + 1
    insertData = FileDcc(file_id=fileId, file_name=namaFile, revision=revision, file_size=sizeFile, file_ext=extFile, permission=permission, parent_path=currentWorkingDirectory, created_by=current_user.nama)
    db.session.add(insertData)
    db.session.commit()
    db.session.close()
    flash('File '+namaFile+' berhasil dibuat')
#
def getPermissionThisFolder(id, folderId, folderName, currentWorkingDirectory):
    fop = db.session.query(FolderDcc.permission).filter(FolderDcc.id == id, FolderDcc.folder_id == folderId, FolderDcc.folder_name == folderName, FolderDcc.parent_path == currentWorkingDirectory, FolderDcc.flag==True).first()
    db.session.close()
    for row in fop:
        permissionIn = row
    return permissionIn
#
def getPermissionDepartemen(permissionIn):
    pdSplit = permissionIn.split( ')(' )
    pd1 = ''
    for row in pdSplit:
        pd1 += row+','
    pd2 = pd1[pd1.find("(")+1:pd1.find(")")]
    permissionDepartemen = pd2.split(',')
    return permissionDepartemen
#
def getOptionDepartemen():
    dept = db.session.query(User.departemen).distinct().all()
    return dept
#
def getNamaFolder(id, folderId):
    nama = db.session.query(FolderDcc.folder_name).filter(FolderDcc.id==id, FolderDcc.folder_id==folderId).first()
    db.session.close()
    for row in nama:
        namaFolder = str(row)
    return namaFolder
#
def updateFolder(id, folderId, namaFolderNew, permission, currentWorkingDirectory):
    oldFolderData = FolderDcc.query.filter_by(id=id, folder_id=folderId, parent_path=currentWorkingDirectory, flag=True).first()
    updateNo = oldFolderData.update_no + 1
    oldFolderData.updated_at = waktuSekarang()
    oldFolderData.updated_by = current_user.nama
    oldFolderData.flag = False
    oldFolderData.status = 'UPDATED'
    db.session.commit()
    db.session.close()
    insertNewData = FolderDcc(folder_id=folderId, folder_name=namaFolderNew, permission = permission, parent_path = currentWorkingDirectory, created_by = current_user.nama, update_no=updateNo)
    db.session.add(insertNewData)
    db.session.commit()
    db.session.close()
#
def changePathFileFolder(oldPath, newPath, strOldPath1, strOldPath2):
    chPathFolder = db.session.query(FolderDcc).filter((FolderDcc.parent_path.like(strOldPath1) | FolderDcc.parent_path.like(strOldPath2)), FolderDcc.flag==True).all()
    for rowFold in chPathFolder:
        pathFold = str(rowFold.parent_path)
        replacedPathFold = pathFold.replace(oldPath, newPath)
        rowFold.parent_path = replacedPathFold
        db.session.commit()
    db.session.close()
    chPathFile = db.session.query(FileDcc).filter((FileDcc.parent_path.like(strOldPath1) | FileDcc.parent_path.like(strOldPath2)), FileDcc.flag==True).all()
    for rowFile in chPathFile:
        pathFile = str(rowFile.parent_path)
        replacedPathFile = pathFile.replace(oldPath, newPath)
        rowFile.parent_path = replacedPathFile
        db.session.commit()
    db.session.close()
#
def getFileNamePermission(fileNameSplit, id, fileId, fileNameIn, currentWorkingDirectory):
    perm = db.session.query(FileDcc.permission).filter(FileDcc.id==id, FileDcc.file_id==fileId, FileDcc.file_name==fileNameIn, FileDcc.parent_path==currentWorkingDirectory, FileDcc.flag==True).first()
    for rowName in fileNameSplit[:-1]:
        fileName = rowName
    for rowPerm in perm:
        permissionIn = rowPerm
    return fileName, permissionIn
#
def getNamaFile(id, fileId, namaFile):
    nama = db.session.query(FileDcc.file_name).filter(FileDcc.id==id, FileDcc.file_id==fileId, FileDcc.flag==True).first()
    db.session.close()
    for rowNama in nama:
        namaFileOld = str(rowNama)
    fileX = db.session.query(FileDcc.file_ext).filter(FileDcc.id==id, FileDcc.file_id==fileId, FileDcc.flag==True).first()
    db.session.close()
    for rowFileX in fileX:
        fileExt = str(rowFileX)
    namaFileNew = namaFile.replace(' ','_')
    namaFileNew = namaFileNew + '.' + fileExt
    return namaFileOld, namaFileNew
#
def updateFile(id, fileId, namaFileNew, permission, currentWorkingDirectory):
    oldFileData = FileDcc.query.filter_by(id=id, file_id=fileId, parent_path=currentWorkingDirectory, flag=True).first()
    updateNo = oldFileData.update_no +1
    oldFileData.updated_at = waktuSekarang()
    oldFileData.updated_by = current_user.nama
    oldFileData.flag = False
    oldFileData.status = 'UPDATED'
    db.session.commit()
    db.session.close()
    insertNewData = FileDcc(file_id=fileId, file_name=namaFileNew, permission = permission, parent_path = currentWorkingDirectory, created_by = current_user.nama, update_no = updateNo)
    db.session.add(insertNewData)
    db.session.commit()
    db.session.close()
#
def deleteFolder(currentWorkingDirectory, id, folderId):
    deleteData = FolderDcc.query.filter_by(id=id, folder_id=folderId, parent_path=currentWorkingDirectory, flag=True).first()
    deleteData.update_no = deleteData.update_no + 1
    deleteData.updated_at = waktuSekarang()
    deleteData.updated_by = current_user.nama
    deleteData.flag = False
    deleteData.status = 'DELETED'
    db.session.commit()
    db.session.close()
#
def deleteFile(currentWorkingDirectory, id, fileId):
    deleteData = FileDcc.query.filter_by(id=id, file_id=fileId, parent_path=currentWorkingDirectory, flag=True).first()
    deleteData.update_no = deleteData.update_no + 1
    deleteData.updated_at = waktuSekarang()
    deleteData.updated_by = current_user.nama
    deleteData.flag = False
    deleteData.status = 'DELETED'
    db.session.commit()
    db.session.close()

### MAIN FUNCTION ###

# Display dokumen menu
def menuDokumen():
    db.session.close()
    root = True
    cwdDcc = model_autentikasi.rootFolderDcc()
    updateVariableUser(cwdDcc, root)

#
def masterDokumen():
    db.session.close()

#
def distribusiDokumen():
    optionDepartemen = getOptionDepartemen()
    cwdDcc = getCwdDcc()
    root = getRootVariable()
    os.chdir(cwdDcc)
    roles = getRoles()

    if roles == 'superadmin' or roles == 'managerdcc':
        fileListQuery = db.session.query(FileDcc.id.label('id'),FileDcc.file_id.label('content_id'),FileDcc.file_name.label('name'), FileDcc.revision, FileDcc.file_size, FileDcc.file_ext, FileDcc.type.label('type')).filter(FileDcc.parent_path==cwdDcc, FileDcc.flag==True)
        folderListQuery = db.session.query(FolderDcc.id.label('id'),FolderDcc.folder_id.label('content_id'),FolderDcc.folder_name.label('name'), db.null(), db.null(), FolderDcc.folder_ext, FolderDcc.type.label('type')).filter(FolderDcc.parent_path==cwdDcc, FolderDcc.flag==True)
        fileList = fileListQuery.union(folderListQuery).order_by('name').all()
        db.session.close()
        return cwdDcc, fileList, root, optionDepartemen
    elif roles == 'user':
        departemen = "%{}%".format(getDepartemen())
        fileListQuery = db.session.query(FileDcc.id.label('id'),FileDcc.file_id.label('content_id'),FileDcc.file_name.label('name'), FileDcc.revision, FileDcc.file_size, FileDcc.file_ext, FileDcc.type.label('type')).filter(FileDcc.parent_path==cwdDcc,(FileDcc.permission.like(departemen))|(FileDcc.permission=='(all)'), FileDcc.flag==True)
        folderListQuery = db.session.query(FolderDcc.id.label('id'),FolderDcc.folder_id.label('content_id'),FolderDcc.folder_name.label('name'), db.null(), db.null(), FolderDcc.folder_ext, FolderDcc.type.label('type')).filter(FolderDcc.parent_path==cwdDcc,(FolderDcc.permission.like(departemen))|(FolderDcc.permission=='(all)'), FolderDcc.flag==True)
        fileList = fileListQuery.union(folderListQuery).order_by('name').all()
        db.session.close()
        return cwdDcc, fileList, root, optionDepartemen

#
def createFolderDcc():
    if request.method == 'POST':
        namaFolder = request.form['nama_folder']
        permissioninput = request.form['folder_permission'].split(',')
        currentWorkingDirectory= request.form['cwd']
        permission = getPermission(permissioninput)
        namaFolder = str(namaFolder)
        folderPath = os.path.join(currentWorkingDirectory, namaFolder)
        os.makedirs(folderPath)
        insertFolderDcc(namaFolder, permission, currentWorkingDirectory)

#
def createFileDcc():
    if request.method == 'POST':
        file = request.files['file']
        revision = request.form['revision']
        permissionInput = request.form['file_permission'].split(',')
        currentWorkingDirectory = request.form['cwd']
        permission = getPermission(permissionInput)

        if file:
            namaFile = secure_filename(file.filename)
            fileSplit = namaFile.split('.')
            extFile = fileSplit[-1]
            fileFolder = os.path.join(currentWorkingDirectory, namaFile)
            file.save(fileFolder)
            sizeFile = os.stat(fileFolder).st_size
            lenSize = len(str(sizeFile))
            if lenSize >= 7:
                sizeFile = sizeFile/(1024*1024)
                sizeFile = float("{0:.2f}".format(sizeFile))
                sizeFile = str(sizeFile) + ' MB'
            elif lenSize >= 4 and lenSize <7:
                sizeFile = sizeFile/1024
                sizeFile = float("{0:.2f}".format(sizeFile))
                sizeFile = str(sizeFile) + ' KB'
            else:
                sizeFile = str(sizeFile) + ' B'

        insertFileDcc(namaFile, revision, sizeFile, extFile, permission, currentWorkingDirectory)

#
def backDirectoryDcc():
    cekRoot = model_autentikasi.rootFolderDcc()
    currentWorkingDirectory = getCwdDcc()
    os.chdir(currentWorkingDirectory)
    os.chdir('..')
    currentWorkingDirectory = os.getcwd()
    if cekRoot == currentWorkingDirectory:
        root = True
        updateVariableUser(currentWorkingDirectory, root)
    else:
        root = False
        updateVariableUser(currentWorkingDirectory, root)

#
def nextDirectoryDcc(item):
    currentWorkingDirectory = getCwdDcc()
    root = False
    os.chdir(currentWorkingDirectory)
    nextDirectory = currentWorkingDirectory + '\\' + item
    os.chdir(nextDirectory)
    currentWorkingDirectory  = nextDirectory
    updateVariableUser(currentWorkingDirectory, root)

#
def openFileDcc(item):
    currentWorkingDirectory = getCwdDcc()
    filePath = os.path.join(currentWorkingDirectory, item)
    fileName = str(item)
    return fileName, filePath

#
def fetchDataFolderDcc():
    if request.method == 'POST':
        id = request.form.get('id')
        folderId = request.form.get('folder_id')
        folderName = request.form.get('folder_name')
        currentWorkingDirectory = getCwdDcc()
        permissionIn = getPermissionThisFolder(id, folderId, folderName, currentWorkingDirectory)
        permissionDepartemen = getPermissionDepartemen(permissionIn)
        optionDepartemen = getOptionDepartemen()
        return id, folderId, folderName, currentWorkingDirectory, permissionDepartemen, optionDepartemen

#
def updateFolderDcc():
    if request.method == 'POST':
        namaFolderNew = request.form['nama_folder']
        permissionInput = request.form['edit_folder_permission'].split(',')
        currentWorkingDirectory = request.form['cwd']
        id = request.form['id']
        folderId = request.form['folder_id']
        namaFolderOld = getNamaFolder(id, folderId)
        permission = getPermission(permissionInput)
        updateFolder(id, folderId, namaFolderNew, permission, currentWorkingDirectory)
        newPath = os.path.join(currentWorkingDirectory, namaFolderNew)
        oldPath = os.path.join(currentWorkingDirectory, namaFolderOld)
        strOldPath1 = '%' + namaFolderOld
        strOldPath2 = '%' + namaFolderOld + '\\\\%'
        os.rename(oldPath, newPath)
        changePathFileFolder(oldPath, newPath, strOldPath1, strOldPath2)

#
def fetchDataFileDcc():
    if request.method == 'POST':
        id = request.form.get('id')
        fileId = request.form.get('file_id')
        fileNameIn =  request.form.get('file_name')
        currentWorkingDirectory = getCwdDcc()
        fileNameSplit = fileNameIn.split('.')
        fileName, permissionIn = getFileNamePermission(fileNameSplit, id, fileId, fileNameIn, currentWorkingDirectory)
        permissionDepartemen = getPermissionDepartemen(permissionIn)
        optionDepartemen = getOptionDepartemen()
        return id, fileId, fileName, currentWorkingDirectory, permissionDepartemen, optionDepartemen

#
def updateFileDcc():
    if request.method == 'POST':
        namaFile = request.form['nama_file']
        permissionInput = request.form['edit_file_permission'].split(',')
        currentWorkingDirectory = request.form['cwd']
        id = request.form['id']
        fileId = request.form['file_id']
        namaFileOld, namaFileNew = getNamaFile(id, fileId, namaFile)
        permission = getPermission(permissionInput)
        updateFile(id, fileId, namaFileNew, permission, currentWorkingDirectory)
        os.rename(namaFileOld, namaFileNew)

#
def deleteFolderDcc(id, folderId, folderName):
    currentWorkingDirectory = getCwdDcc()
    folderPath = os.path.join(currentWorkingDirectory, folderName)
    cekParentFold = FolderDcc.query.filter_by(parent_path=folderPath, flag=True).first()
    cekParentFile = FileDcc.query.filter_by(parent_path=folderPath, flag=True).first()
    if cekParentFold or cekParentFile:
        # flash('kosongkan terlebih dahulu foldernya')
        print('kosongkan terlebih dahulu foldernya')
    else:
        deleteFolder(currentWorkingDirectory, id, folderId)
        os.rmdir(folderPath)
        # flash('folder removed')
        print('folder removed')
#
def deleteFileDcc(id, fileId, fileName):
    currentWorkingDirectory = getCwdDcc()
    filePath = os.path.join(currentWorkingDirectory, fileName)
    deleteFile(currentWorkingDirectory, id, fileId)
    os.remove(filePath)
    # flash('file Removed')
    print('file Removed')