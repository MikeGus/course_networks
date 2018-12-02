import os
import shutil
from appconfig import app, UPLOAD_FOLDER
from flask import render_template, request, abort, send_file, redirect
from utils import render_directory

from models import *


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def get_directory_content_or_upload(path):
    full_path = os.path.join(os.curdir, UPLOAD_FOLDER, path)

    if request.method == 'POST':
        file = request.files['file']
        if file and os.path.isdir(full_path):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], path, filename))
            filename, extension = os.path.splitext(filename)
            db_stats, created = TypeStat.get_or_create(extension=extension)
            db_stats.uploads += 1
            db_stats.save()
            return render_directory(full_path)
        abort(403)

    if os.path.isdir(full_path):
        app.config['PREV_FOLDER'] = path
        return render_directory(full_path)
    elif os.path.isfile(full_path):
        filename, extension = os.path.splitext(full_path)
        db_stats, created = TypeStat.get_or_create(extension=extension)
        db_stats.downloads += 1
        db_stats.save()
        return send_file(full_path, attachment_filename='path')

    abort(404)


@app.route('/add_folder', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>/add_folder', methods=['POST'])
def add_folder(path):
    full_path = os.path.join(os.curdir, UPLOAD_FOLDER, path)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        abort(404)
    try:
        if request.form['new_folder'] is not '' and not (path == '' and request.form['new_folder'] == 'info'):
            full_path = os.path.join(os.curdir, UPLOAD_FOLDER, path, request.form['new_folder'])
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        return redirect(app.config['PREV_FOLDER'])
    except OSError:
        abort(400)


@app.route('/<path:path>/rename', methods=['POST'])
def rename_path(path):
    full_path = os.path.join(os.curdir, UPLOAD_FOLDER, path)
    if not os.path.exists(full_path):
        abort(404)
    if request.form['new_filename'] is not '' and not (path == '' and request.form['new_filename'] == 'info'):
        new_full_path = os.path.join(os.curdir, UPLOAD_FOLDER, app.config['PREV_FOLDER'], request.form['new_filename'])
        try:
            os.rename(full_path, new_full_path)
            return redirect(app.config['PREV_FOLDER'])
        except OSError:
            abort(400)
    return redirect(app.config['PREV_FOLDER'])


@app.route('/<path:path>/delete', methods=['POST'])
def delete_path(path):
    full_path = os.path.join(os.curdir, UPLOAD_FOLDER, path)
    if not os.path.exists(full_path):
        abort(404)
    try:
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
        return redirect(app.config['PREV_FOLDER'])
    except OSError:
        abort(400)


@app.route('/info', methods=['GET'])
def get_info():
    info = TypeStat.select()
    for element in info:
        if element.extension == '':
            element.extension = '<None>'
    return render_template('info.html', info=info)
