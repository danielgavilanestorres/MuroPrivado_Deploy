from operator import imod
import bcrypt
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "dfdfgg34543dfgdgser"
bcrypt = Bcrypt(app)