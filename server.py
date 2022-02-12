from os import environ
import Flask from flask 
app = Flask(__name__) app.run(environ.get('PORT')) 