import os
import datetime
import flask

app = flask.Flask(__name__)

ROOT='static'
MONTHS = dict(zip(range(1, 13), 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()))
FMT = '<a href="{}">{:<55}{:0>2}-{}-{} {:0>2}:{:0>2}{:>20}'

def list_files(pathname):
    for filename in os.listdir(pathname):
        absname = flask.safe_join(pathname, filename)

        if os.path.isfile(absname):
            filesize = str(os.path.getsize(absname))
        else:
            # else if directory
            filesize = '-'
            filename += '/'

        dtime = datetime.datetime.fromtimestamp(os.path.getmtime(absname))
        lines = FMT.format(
            absname[len(ROOT):], # remove 'static/' from absolute path
            filename + '</a>', # escape <a>
            dtime.day,
            MONTHS[dtime.month],
            dtime.year,
            dtime.hour,
            dtime.minute,
            filesize
        )

        yield flask.Markup(lines)

@app.route('/', defaults={'path': None})
@app.route('/<path:path>')
def home(path):
    
    pathname = ROOT if path is None else flask.safe_join(ROOT, path)

    if os.path.isdir(pathname):
        return flask.render_template('home.html', pathname=pathname[len(ROOT):], dircontents=list_files(pathname))
    elif os.path.isfile(pathname):
        return flask.send_file(pathname)
    else:
        return flask.abort(404)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)