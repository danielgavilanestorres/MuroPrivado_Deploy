from flask import redirect, request
from flask_app import app
from flask_app.models.mensaje import Mensaje

@app.route('/Eliminar/Mensaje/<int:id>')
def EliminarMensaje(id):
    Mensaje.EliminarMensajesRecibidos({'id': id})
    return redirect('/Muro')

@app.route('/Enviar/Mensaje', methods=['post'])
def EnviarMensaje():
    Mensaje.EnviarMensaje({'contenido': request.form['contenido'], 'usuarioIdDe': request.form['usuarioIdDe'], 'usuarioIdPara': request.form['usuarioIdPara']})
    return redirect('/Muro')