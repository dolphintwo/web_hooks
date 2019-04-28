from flask import Flask,request,url_for,abort
import os
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    os.system('echo "[`date +%Y-%m-%d/%H:%M:%S`] GET /" >> ./web_hooks.log')
    return "Hello!"

@app.route("/gitee", methods=["POST"])
def gitee():
    if 'User-Agent' in request.headers:
        if request.headers.get('User-Agent') == 'git-oschina-hook':
            if request.headers.get('X-Gitee-Token') == 'dbce613a94b51bcba5bb381983653613':
                os.system('/bin/sh ./scripts/redeploy.sh')
                return "success!"
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)

@app.errorhandler(403)
def forbidden(error):
    return "Forbidden\n"

@app.errorhandler(404)
def page_not_found(error):
    return "NOT FOUND\n"

@app.errorhandler(405)
def page_not_found(error):
    return "Method Not Allowed\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
