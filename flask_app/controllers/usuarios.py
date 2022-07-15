import bcrypt
from flask import flash, redirect, render_template, request, session
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from flask_app.models.mensaje import Mensaje

#RUTA RAIZ
@app.route('/')
def Raiz():
    return render_template("Inicio.html")

#REGISTRO NUEVO USUARIO
@app.route('/Registro/Usuario', methods = ['post'])
def RegistrarUsuario():
    if not Usuario.ValidarUsuario(request.form):
        return redirect('/')
    claveHash = bcrypt.generate_password_hash(request.form['clave'])
    dicUsuario = {'nombre': request.form['nombre'], 'apellido': request.form['apellido'], 'correo': request.form['correo'], 'clave': claveHash}
    session['usuarioId'] = Usuario.RegistrarUsuario(dicUsuario)
    return redirect('/Muro')

#ACCESO A MURO
@app.route('/Muro')
def Muro():
    if 'usuarioId' not in session:
        return redirect('/')
    return render_template("Muro.html", usuario = Usuario.VerUsuarioPorId({'usuarioId': session['usuarioId']}), 
                                        numMensajes = Mensaje.NumeroMensajesRecibidos({'usuarioIdPara': session['usuarioId']}),
                                        listaMensajes = Mensaje.MensajesRecibidos({'usuarioIdPara': session['usuarioId']}),
                                        listaUsuarios = Usuario.UsuariosParaEnviarMensajes({'usuarioId': session['usuarioId']}))

#INICIAR SESION
@app.route('/Iniciar/Sesion', methods = ['post'])
def IniciarSesion():
    usuarioEncontrado = Usuario.UsuarioPorCorreo({'correo': request.form['correo']})
    if not usuarioEncontrado:
        flash("Correo/Clave Invalidos", "validacion2")
        return redirect('/')
    if not bcrypt.check_password_hash(usuarioEncontrado.clave, request.form['clave']):
        flash("Correo/Clave Invalidos", "validacion2")
        return redirect('/')
    session['usuarioId'] = usuarioEncontrado.id
    return redirect('/Muro')

#CERRAR SESION
@app.route('/Cerrar/Sesion')
def CerarSesion():
    session.clear()
    return redirect('/')

