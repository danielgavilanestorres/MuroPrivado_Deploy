import pymysql.cursors

class conexionMySQL:
    def __init__(self, baseDatos):
        conexion = pymysql.connect(host='localhost', user='root', password='snoppy88', db=baseDatos, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        self.conexion = conexion

    def operacionBD(self, query, data = None):
        with self.conexion.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Corriendo Consulta: ", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.conexion.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.conexion.commit()
            except Exception as e:
                print("Algo esta Mal: ", e)
            finally:
                self.conexion.close()
    
def conectarMySQL(baseDatos):
    return conexionMySQL(baseDatos)
