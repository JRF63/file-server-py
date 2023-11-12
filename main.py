import datetime
import os
import sys

import flask
from werkzeug.utils import safe_join

app = flask.Flask(__name__)

DEFAULT_PATH = 'static'
MONTHS = dict(zip(range(1, 13), 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()))
MAX_FILE_NAME_LEN = 50
FMT = '<a href="{}">{:<%d} {:0>2}-{}-{} {:0>2}:{:0>2}{:>20}' % (MAX_FILE_NAME_LEN + len('</a>'))

def list_files(server_path):
    for file_name in os.listdir(server_path):
        absname = safe_join(server_path, file_name)

        if os.path.isfile(absname):
            filesize = str(os.path.getsize(absname))
        else:
            # else if directory
            filesize = '-'
            file_name += '/'

        dtime = datetime.datetime.fromtimestamp(os.path.getmtime(absname))

        link_text = file_name
        if len(file_name) > MAX_FILE_NAME_LEN:
            link_text = file_name[:(MAX_FILE_NAME_LEN - 3)] + '...'

        lines = FMT.format(
            # relative path
            file_name,
            # escapes <a>; must put </a> here instead of inside `FMT` to
            # prevent the ugly inclusion of spaces in the hyperlink
            link_text + '</a>', 
            dtime.day,
            MONTHS[dtime.month],
            dtime.year,
            dtime.hour,
            dtime.minute,
            filesize
        )

        yield flask.Markup(lines)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    root = flask.current_app.config['root']
    server_path = safe_join(root, path)

    if os.path.isdir(server_path):
        # Force displaying the root, /
        pathname = '/' if path == '' else path
        return flask.render_template('home.html', pathname=pathname, dircontents=list_files(server_path))
    elif os.path.isfile(server_path):
        return flask.send_file(server_path)
    else:
        return flask.abort(404)
    
if __name__ == '__main__':
    app.config['root'] = DEFAULT_PATH
    if len(sys.argv) > 1:
        app.config['root'] = sys.argv[1]
    app.run(host='0.0.0.0', port='8080', debug=True)