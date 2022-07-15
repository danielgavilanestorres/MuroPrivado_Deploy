from flask_app import app, bcrypt
from flask_app.controllers import usuarios, mensajes

if __name__ == "__main__":
    app.run(debug = True)