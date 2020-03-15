# API_REST Hospitales


## Descripcion

Servicio web (API REST), que sirve de endpoints para un sistema de gestion de historia clinica centralizada, utilizando Phyton con Flask, y PostgreSQL como motor de la base de datos.

## Como instalar

* Base de datos:
  * `/modelos/engine/dbstorage.py`
  * configurar el metodo `__init__` en la linea `self.__engine = db.create_engine('postgresql://usuario:password@localhost/API_REST_HOSPITAL')`,
  poner su usario y password de postgres
  
* Dependencias:

  * `requirements.txt`
  * Para instalar todos los paquetes de python necesarios para correr la api, recomiendo crear un entorno virtual
  `python3 -m venv nombredelentorno` y puego `source /nombredelentorno/bin/activate`
  * luego dentro del entorno ejecutar `pip install -r requirements.txt`

## modulos y archivos

   * `/modelos`: En este paquete se encuentran declaradas todas las clases usadas en la api.
   * `/modelos/engine`: Aqui se encuentra el modulo `dbstorage.py` encargado de
   conectarse con la base de datos y gestionar todos los objetos en ella.
   * `/api/v1`: Se encuentra el modulo app.py en el que se inicia la API, y se
   conecta con todas las Blueprints y metodos de la API.


## Metodos

   * Registar Usuarios: de entrada la API permite registrar dos tipos de usuario
   `hospital` y `paciente`, ademas crea un link para autenticar el registro por
   medio del correo.
   
   * Registrar Paciente:
   ```http
   POST /api/v1/register 
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
   "usuario" : "paciente",
   "formulario" : {
   		  "nombre": string,
		  "id": string,
		  "password": string,
		  "correo": string,
		  "telefono": string,
		  "direccion": string,
		  "fecha_nacimiento": string
   		  }
   }
   ```
   
   * Registrar Hospital:
   ```http
   POST /api/v1/register 
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
   "usuario" : "hospital",
   "formulario" : {
   		  "nombre": string,
		  "id": string,
		  "password": string,
		  "correo": string,
		  "telefono": string,
		  "direccion": string,
   		  },
   "servicios" : ["string", "string", ...]   	          		  
   }
   ```

   * Login Usuarios: para hacer login es necesario haberse verificado con el
   correo.
   ```http
   POST /api/v1/login 
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
   "id" : string,
   "password" : string, 
   }
   ```
   Retorna un token para el acceso al sistema.
   ```
   {"id" : "token"}
   ```

   * Reiniciar password: crea un link para reiniciar el password con el correo.
   ```http
   POST /api/v1/reset_password
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
    "correo": string,
   }
   ```
   
## Metodos con uso del tokem o con usuario autenticado

Cada que un usuario hace login y este es exitoso la api retorna un token
que se debe enviar en los headers como:
   `"Authorization: Bearer token"`
todos los metodos que siguen acontinuacion utilizan este token para funcionar.

   * Registrar medicos: Solo los usuarios de tipo Hospital pueden registrar
   un nuevo medico.
   ```http
   POST /api/v1/registrar_medico 
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
   "usuario" : "paciente",
   "formulario" : {
   		  "nombre": string,
		  "id": string,
		  "password": string,
		  "correo": string,
		  "telefono": string,
		  "direccion": string,
		  "especialidad": string
   		  }
   }
   ```

   * Registrar Observacion: Solo los usuarios de tipo Medico pueden registrar
   una observacion de sus pacientes.
   ```http
   PUT /api/v1/registrar_observacion 
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
   "formulario" : {
   		  "paciente_id": string,
		  "registro": string,
		  }
   }
   ```

   * Consultar registros: Un usuario de tipo Paciente puede consultar solo
   sus registros, uno de tipo Medico solo puede consultar los registros
   realizados por el mismo y un usuario de tipo Hospital solo puede consultar
   los registros realizados por sus medicos.
   ```http
   GET /api/v1/consultar
   ```
   Retorna un diccionario de tipo JSON con los registros.

   * Descargar registros: Un usuario de tipo medico puede descargar todas
   las observaciones registradas a un paciente en formato csv.
   ```http
   GET /descargar_consulta/<paciente_id>
   ```
   retorna un archivo en formato csv.

   * Cambiar password:
   ```http
   POST /api/v1/change_password
   ```
   Recibe los siguientes parametros:
   ```javascript
   {
    "old_password": string,
    "new_passwor": string,
   }
   ```
   
## Status Codigos

La API retorna los siguientes codigos de status:

| Status Codigo | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 401 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |



## Autor

* Diego Vivas, [@diegovivas](https://github.com/diegovivas)
