
#Lenguaje DML (Lenguaje de manipulación de datos)
class UsuarioRepository:
    def __init__(self, connection):
        self.connection = connection

    def buscar_por_email(self, email):
        cursor = self.connection.cursor() #Crea el cursor, quien ejecuta las consultas SQL
        try:
            sql = """
                SELECT 
                    id,
                    email,
                    password_hash,
                    nombres,
                    apellidos,
                    rol,
                    estado
                FROM usuario
                WHERE email = %s
                LIMIT 1
            """
            cursor.execute(sql, (email,))
            return cursor.fetchone() #Toma la primera fila y devuelve un diccionario
        finally:
            cursor.close()

    def buscar_por_id(self, usuario_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                SELECT 
                    id,
                    email,
                    nombres,
                    apellidos,
                    rol,
                    estado,
                    fecha_registro
                FROM usuario
                WHERE id = %s
                LIMIT 1
            """
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def guardar(self, usuario):
        cursor = self.connection.cursor()
        try:
            sql = """
                INSERT INTO usuario (email, password_hash, nombres, apellidos, rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.get('email'),
                usuario.get('password_hash'),
                usuario.get('nombres'),
                usuario.get('apellidos'),
                usuario.get('rol', 'usuario'),
                usuario.get('estado', 1)
            ))
            self.connection.commit()
            return cursor.lastrowid
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()


    def guardar_usuario(self, usuario):
        cursor = self.connection.cursor()
        try:
            sql = """
                INSERT INTO usuario (email, password_hash, nombres, apellidos, rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.get('email'),
                usuario.get('password_hash'),
                usuario.get('nombres'),
                usuario.get('apellidos'),
                usuario.get('rol', 'usuario'),
                usuario.get('estado', 1)
            ))
            return cursor.lastrowid
        finally:
            cursor.close()

    def guardar_pasajero(self, id_usuario):
        cursor = self.connection.cursor()
        try:
            sql = """
                INSERT INTO pasajero (usuario_id)
                VALUES (%s)
            """
            cursor.execute(sql, (
                id_usuario,
            ))
            
            return cursor.lastrowid
        finally:
            cursor.close()

    def guardar_conductor(self, id_usuario, licencia, calificacion):
        cursor = self.connection.cursor()
        try:
            sql = """
                INSERT INTO conductor (usuario_id,licencia, calificacion)
                VALUES (%s,%s,%s)
            """
            cursor.execute(sql, (
                id_usuario,
                licencia,
                calificacion
            ))
            self.connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()