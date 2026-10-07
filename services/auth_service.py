from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from database import get_connection
from repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash

class AuthService:
    def login(self, email, password):
        connection = get_connection()
        try:
            repository = UsuarioRepository(connection)
            usuario = repository.buscar_por_email(email)


            #El usuario existe en la BD?
            if usuario is None:
                return None, "Correo o contraseña incorrectos", 401

            #El usuario esta activo en la BD?

            if usuario["estado"] != "ACTIVO":
                return None, "El usuario se encuentra inactivo", 403

            #La contraseña que se envia y la del usuario es la misma con hash?

            if not check_password_hash(
                usuario["password_hash"],
                password
            ):
                return None, "Correo o contraseña incorrectos", 401

            #Si no existe ningún problema, se crea el token de acceso JWT

            token = create_access_token(
                identity=str(usuario["id"]),
                additional_claims={
                    "rol": usuario["rol"]
                }
            )

            #Se forma el diccionario que tendra los datos del usuario
            #Y además tendra el token de acceso

            data = {
                "usuario id": usuario["id"],
                "email": usuario["email"],
                "nombres": usuario["nombres"],
                "apellidos": usuario["apellidos"],
                "rol": usuario["rol"],
                "estado": usuario["estado"],
                "token": token
            }

            return data, "Inicio de sesión satisfactorio", 200

        finally:
            connection.close()

    def register(self, email, password, nombres, apellidos, rol,licencia, calificacion):
        connection = get_connection()

        roles_permitidos =["PASAJERO","CONDUCTOR","ADMINISTRADOR"]
        
        try:
            repository = UsuarioRepository(connection)
            usuario = repository.buscar_por_email(email)

            #El usuario existe en la BD?
            if usuario is not None:
                return None, "El usuario ya esta registrado en la BD con este correo", 409


            if str(rol).upper() in roles_permitidos:
                print("Escogio un rol permitido: ")
            else:
                return None, "Se debe escoger un rol permitido", 401


           #Vamos a registrar al usuario, formando un diccionario de datos

            data_real = {
               "email":email,
               "password_hash": generate_password_hash(password),
               "nombres":nombres,
               "apellidos":apellidos,
               "rol":rol,
               "estado":"ACTIVO"
            }

            #Llamamos al método que inserta datos

            id_usuario = repository.guardar_usuario(data_real)


            if id_usuario is None:
                return None, "Error el insertar un nuevo usuario",400

            #Si elige pasajero se tiene que insertar ne la tabla
            id_usuario_pasajero=""
            id_usuario_conductor=""

            if str(rol).upper() == "PASAJERO":
                 print("Insertar en la tabla pasajero")
                 id_usuario_pasajero = repository.guardar_pasajero(id_usuario)

            if str(rol).upper() == "CONDUCTOR":
                print("Insertar en la tabla conductor")
                id_usuario_conductor = repository.guardar_conductor(id_usuario, licencia, calificacion)

            connection.commit()


            data_nueva ={
                "id_usuario":id_usuario,
                "id_usuario_pasajero":id_usuario_pasajero,
                "id_usuario_conductor":id_usuario_conductor
            }

            return data_nueva, "Registro Exitoso satisfactorio, con su respectivo ROL", 201

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()