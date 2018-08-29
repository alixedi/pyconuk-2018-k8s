import code
import io
import contextlib

import flask

app = flask.Flask(__name__)
app.console = None


class WebConsole:

    def __init__(self):
        self.console = code.InteractiveConsole()

    def run(self, code):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with contextlib.redirect_stderr(output):
                for line in code.splitlines():
                    self.console.push(line)
        return {'output': str(output.getvalue())}


@app.route('/run/', methods=['POST'])
def run():
    if app.console is None:
        app.console = WebConsole()
    return flask.jsonify( 
        app.console.run(
            flask.request.get_json()['input']
        )
    )

