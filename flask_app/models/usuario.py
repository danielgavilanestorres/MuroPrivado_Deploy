from flask import flash, request
import re
from flask_app.config.mysqlconnection import conectarMySQL

correoRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
claveRegex = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

class Usuario:
    db = "muroprivado"
    def __init__(self, datosUsuario):
        self.id = datosUsuario['id']
        self.nombre = datosUsuario['nombre']
        self.apellido = datosUsuario['apellido']
        self.correo = datosUsuario['correo']
        self.clave = datosUsuario['clave']
        self.fechaCreacion = datosUsuario['fechaCreacion']
        self.fechaActualizacion = datosUsuario['fechaActualizacion']
        self.listaMensajes = []
    
    @staticmethod
    def ValidarUsuario(usuarioForm):
        esValido = True
        consultaSQL = "select * from usuarios where correo = %(correo)s;"
        resultadoSQL = conectarMySQL("muroprivado").operacionBD(consultaSQL, usuarioForm)
        if len(usuarioForm['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "validacion1")
            esValido = False
        if len(usuarioForm['apellido']) < 3:
            flash("El apellido debe tener al menos 3 caracteres", "validacion1")
            esValido = False
        if len(usuarioForm['correo']) < 3:
            flash("El correo debe tener al menos caracteres", "validacion2")
            esValido = False
        if not correoRegex.match(request.form['correo']):
            flash("El correo ingresado no es valido", "validacion2")
            esValido = False
        if len(resultadoSQL) >= 1:
            flash("El correo ingresado ya esta registrado", "validacion2")
            esValido = False
        if len(request.form['clave']) < 9:
            flash("La contraseña debe tener al menos 8 caracteres", "validacion2")
            esValido = False
        if not claveRegex.match(request.form['clave']):
            flash("La clave no cumple con los requisitos minimos", "validacion2")
            esValido = False
        if not request.form['clave'] == request.form['claveOk']:
            flash("Las constraseñas no coinciden", "validacion2")
            esValido = False
        return esValido
    
    @classmethod
    def RegistrarUsuario(cls, dicUsuario):
        consultaSQL = "insert into usuarios(nombre, apellido, correo, clave) values(%(nombre)s, %(apellido)s, %(correo)s, %(clave)s);"
        return conectarMySQL(cls.db).operacionBD(consultaSQL, dicUsuario)
    
    @classmethod
    def VerUsuarioPorId(cls, dicIdUsuario):
        consultaSQL = "select * from usuarios where id = %(usuarioId)s;"
        resultadoSQL = conectarMySQL(cls.db).operacionBD(consultaSQL, dicIdUsuario)
        if len(resultadoSQL) < 1:
            return False
        return cls(resultadoSQL[0])
    
    @classmethod
    def UsuarioPorCorreo(cls, dicCorreoUsuario):
        consultaSQL = "select * from usuarios where correo = %(correo)s;"
        resultadoSQL = conectarMySQL(cls.db).operacionBD(consultaSQL, dicCorreoUsuario)
        if len(resultadoSQL) < 1:
            return False
        return cls(resultadoSQL[0])
    
    @classmethod
    def UsuariosParaEnviarMensajes(cls, dicIdUsuario):
        consultaSQL = "select id, nombre, apellido from usuarios where id != %(usuarioId)s;"
        resultadoSQL = conectarMySQL(cls.db).operacionBD(consultaSQL, dicIdUsuario)
        listaUsuarios = []
        for usuario in resultadoSQL:
            listaUsuarios.append(usuario)
        return listaUsuarios