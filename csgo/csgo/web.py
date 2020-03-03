import os
import subprocess
import sys

from flask import Flask, request, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)


@app.route('/v2/api/5e', methods=['get', 'post'])
def a5e():
    domain = request.args.get('domain')
    command = 'scrapy crawl 5e -a domain=' + domain
    command = command.split(" ")
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return json.dumps({
            'code': 1
        })
    except subprocess.CalledProcessError as exc:
        return json.dumps({
            'code': 0
        })
        # print('returncode:', exc.returncode)
        # print('cmd:', exc.cmd)
        # print('output:', exc.output.decode("gbk"))


@app.route('/v2/api/b5', methods=['get', 'post'])
def b5():
    steamid = request.args.get('steamid')
    command = 'scrapy crawl b5 -a steamid=' + steamid
    command = command.split(" ")
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return json.dumps({
            'code': 1
        })
    except subprocess.CalledProcessError as exc:
        return json.dumps({
            'code': 0
        })


if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False, port=8092)
