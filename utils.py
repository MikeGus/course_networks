import os
from flask import request, render_template


def get_parent_url(url, base):
    if url == base:
        return base
    i = -1
    while url[i] != '/' and len(url) + i > len(base):
        i -= 1
    return url[:i]


def render_directory(path):
    files = os.listdir(path)
    filenames = [os.path.join(request.url, file) for file in files]
    files.sort()
    filenames.sort()
    parent = get_parent_url(request.url, request.url_root)
    url = request.url
    if url[-1] is not '/':
        url += '/'
    return render_template('directory.html',
                           files=files,
                           filenames=filenames,
                           length=len(filenames),
                           url=url,
                           parent=parent)
