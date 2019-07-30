import os
import datetime
import flask

app = flask.Flask(__name__)

ROOT='static'
MONTHS = dict(zip(range(1, 13), 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()))

def get_metadata(absname):
    filesize = os.path.getsize(absname) if os.path.isfile(absname) else '-'
    meta_fmt = '{:0>2}-{}-{} {:0>2}:{:0>2}{:>20}'

    mtime = os.path.getmtime(absname)
    dtime = datetime.datetime.fromtimestamp(mtime)
    metadata = meta_fmt.format(
        dtime.day,
        MONTHS[dtime.month],
        dtime.year,
        dtime.hour,
        dtime.minute,
        filesize
    )
    return metadata

@app.route('/', defaults={'path': None})
@app.route('/<path:path>')
def home(path):
    
    if path is None:
        pathname = ROOT
    else:
        pathname = flask.safe_join(ROOT, path)
    if os.path.isdir(pathname):
        def list_files():
            for filename in os.listdir(pathname):
                absname = flask.safe_join(pathname, filename)

                num_spaces = max(51 - len(filename), 1)
                metadata = get_metadata(absname)
                metadata = (' ' * num_spaces) + metadata

                yield (absname[7:], filename, metadata)

        return flask.render_template('home.html', path=pathname, dircontents=list_files())
    elif os.path.isfile(pathname):
        return flask.send_file(pathname)
    else:
        return flask.abort(404)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)