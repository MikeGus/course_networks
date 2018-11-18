from flask import Flask, send_file, abort, render_template, request
import os
import shutil

app = Flask(__name__)


def render_directory(path):
    files = os.listdir(path)
    filenames = [os.path.join(request.url, file) for file in files]
    files.sort()
    filenames.sort()
    length = len(files)
    return render_template('directory.html',
                           files=files,
                           filenames=filenames,
                           length=length)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def get_file_or_directory_content(path):
    full_path = os.path.join(os.curdir, 'static', path)

    if os.path.isdir(full_path):
        return render_directory(full_path)
    elif os.path.isfile(full_path):
        return send_file(full_path, attachment_filename='path')

    abort(404)


@app.route('/<path:path>/rename', methods=['POST'])
def rename_path(path):
    full_path = os.path.join(os.curdir, 'static', path)
    if not os.path.exists(full_path):
        abort(404)
    new_full_path = os.path.join(os.curdir, 'static', request.json['name'])
    try:
        os.rename(full_path, new_full_path)
        return get_file_or_directory_content(os.path.join(os.path.dirname(path), request.json['name']))
    except OSError:
        abort(400)


@app.route('/<path:path>', methods=['DELETE'])
def delete_path(path):
    full_path = os.path.join(os.curdir, 'static', path)
    if not os.path.exists(full_path):
        abort(404)
    try:
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
        return get_file_or_directory_content(os.path.dirname(full_path).replace('./static', ''))
    except OSError:
        abort(400)


if __name__ == '__main__':
    app.run()
