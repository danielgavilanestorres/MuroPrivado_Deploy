from datetime import date, datetime
import math
from flask_app.config.mysqlconnection import conectarMySQL

class Mensaje:
    db = "muroprivado"
    def __init__(self, datosMensaje):
        self.id = datosMensaje['id']
        self.contenido = datosMensaje['contenido']
        self.usuarioIdDe = datosMensaje['usuarioIdDe']
        self.nombreDe = datosMensaje['nombreDe']
        self.apellidoDe = datosMensaje['apellidoDe']
        self.usuarioIdPara = datosMensaje['usuarioIdPara']
        self.nombrePara = datosMensaje['nombrePara']
        self.apellidoPara = datosMensaje['apellidoPara']
        self.fechaCreacion = datosMensaje['fechaCreacion']
        self.fechaActualizacion = datosMensaje['fechaActualizacion']
    
    def tiempo(self):
        now = datetime.now()
        hace = now - self.fechaCreacion
        if hace.days > 0:
            return f"hace {hace.days}s"
        elif (math.floor(hace.total_seconds() / 60)) >= 60:
            return f"Hace {math.floor(math.floor(hace.total_seconds() / 60)/60)} horas"
        elif hace.total_seconds() >= 60:
            return f"Hace {math.floor(hace.total_seconds() / 60)} minutos"
        else:
            return f"Hace {math.floor(hace.total_seconds())} segundos"
    
    @classmethod
    def NumeroMensajesRecibidos(cls, dicIdPara):
        consultaSQL = "select count(*) from mensajes where usuarioIdPara = %(usuarioIdPara)s;"
        resultadoSQL = conectarMySQL(cls.db).operacionBD(consultaSQL, dicIdPara)
        return resultadoSQL[0]['count(*)']
    
    @classmethod
    def MensajesRecibidos(cls, dicIdPara):
        consultaSQL = "select m.id as id, m.contenido as contenido, u.id as usuarioIdDe, u.nombre as nombreDe, u.apellido as apellidoDe, m.usuarioIdPara as usuarioIdPara, u2.nombre as nombrePara, u2.apellido as apellidoPara, m.fechaCreacion as fechaCreacion, m.fechaActualizacion as fechaActualizacion from usuarios as u inner join mensajes as m on u.id = m.usuarioIdPara inner join usuarios as u2 on u2.id = m.usuarioIdDe  where m.usuarioIdPara = %(usuarioIdPara)s;"
        resultadoSQL = conectarMySQL(cls.db).operacionBD(consultaSQL, dicIdPara)
        mensajes = []
        for mensaje in resultadoSQL:
            mensajes.append(cls(mensaje))
        return mensajes
    
    @classmethod
    def EliminarMensajesRecibidos(cls, dicIdMensaje):
        consultaSQL = "delete from mensajes where id = %(id)s;"
        return conectarMySQL(cls.db).operacionBD(consultaSQL, dicIdMensaje)
    
    @classmethod
    def EnviarMensaje(cls, dicMensaje):
        consultaSQL = "insert into mensajes(contenido, usuarioIdDe, usuarioIdPara) values (%(contenido)s, %(usuarioIdDe)s, %(usuarioIdPara)s);"
        return conectarMySQL(cls.db).operacionBD(consultaSQL, dicMensaje)