from flask import Flask, request
import json

from util.cross_origin import MyResponse

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Hello World!'


def start_flask():
    app.response_class = MyResponse
    app.run(debug=True, host="0.0.0.0", port=8088, threaded=True, use_reloader=False)


if __name__ == '__main__':
    start_flask()
