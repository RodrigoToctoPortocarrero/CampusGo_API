from flask import Blueprint, request #Llama a request y al agrupador de rutas

from services.auth_service import AuthService #Llama a la clase definida en el servicio
from utils.response import success_response, error_response #Definición de respuestas

#Positiva o negativo

auth_bp = Blueprint("auth", __name__) #Creación del conjunto de rutas

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) #Obtener el formato JSON

    if datos is None:
        return error_response(
            "Debe enviar los datos en formato JSON",
            400
        )

    email = str(datos.get("email", "")).strip() #Como el método .trim() de java
    password = str(datos.get("password", ""))


    #Comprobar si alguno de los dos esta vacio (not)
    if not email or not password:
        return error_response(
            "Email y password son obligatorios",
            400
        )

    service = AuthService()

    data, message, http_code = service.login(
        email,
        password
    )

    if data is None:
        return error_response(message, http_code)

    return success_response(
        data,
        message,
        http_code
    )


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    datos = request.get_json(silent=True) #Obtener el formato JSON

    if datos is None:
        return error_response(
            "Debe enviar los datos en formato JSON",
            400
        )

    email = str(datos.get("email", "")).strip() #Como el método .trim() de java
    password = str(datos.get("password", ""))
    nombres = str(datos.get("nombres","")).strip()
    apellidos = str(datos.get("apellidos","")).strip()
    rol = str(datos.get("rol","")).strip() #Validar que solo sean
    licencia = str(datos.get("licencia","")).strip()
    calificacion = float(datos.get("calificacion",0))


    #Comprobar si alguno de los dos esta vacio (not)
    if not email or not password or not nombres or not apellidos or not rol:
        return error_response(
            "Todos los campos son obligatorios",
            400
        )

    if rol == "CONDUCTOR":
        if not licencia or not calificacion:
            return error_response(
                "Si es conductor, la licencia y calificación son obligatorios",
                400
            )


    service = AuthService()

    #Llamamos al método register del servicio AuthService

    data, message, http_code = service.register(
        email,
        password,
        nombres,
        apellidos,
        rol,
        licencia,
        calificacion
    )

    if data is None:
        return error_response(message, http_code)

    return success_response(
        data,
        message,
        http_code
    )




    

