import sys, code, io, json, contextlib

import flask


app = flask.Flask(__name__)
app.consoles = {}


class WebConsole():

    def __init__(self):
        self.console = code.InteractiveConsole()

    def run(self, code):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with contextlib.redirect_stderr(output):
                for line in code.splitlines():
                    self.console.push(line)
        return {'output': str(output.getvalue())}


@app.route('/run/<uname>', methods=['POST'])
def run(uname):
    if not uname in app.consoles:
        app.consoles[uname] = WebConsole()
    return flask.jsonify( 
        app.consoles[uname].run(
            flask.request.get_json()['input']
        )
    )

