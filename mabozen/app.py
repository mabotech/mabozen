
"""
Web UI for mabozen
- config
- code gen
- model dump
- db object backup and sync
...
"""

from time import localtime, strftime
import subprocess

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    """ show app info """
    data = {"app":"mabozen", "time":strftime("%Y-%m-%d %H:%M:%S", localtime()) }
    return jsonify(data)

@app.route("/web")
def web():
    """ gen web code """
    return "web gen"
    
@app.route("/model")
def model():
    """ gen model """
    return "model"
    
@app.route("/backup")
def backup():
    """ backup db """
    return "backup"

if __name__ == "__main__":
    
    #install package when nodemon restart app
    subprocess.Popen("python setup.py install", shell="True")
    
    app.run(port=7000)