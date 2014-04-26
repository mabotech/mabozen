
import subprocess

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return {"app":"mabozen"}

if __name__ == "__main__":
    
    subprocess.Popen("python setup.py install", shell="True")
    
    app.run(port=7000)