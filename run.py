from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    send_from_directory,
    url_for,
    session,
    flash,)
from flask_mysqldb import MySQL
from flask_login import current_user, login_required, LoginManager, login_user, login_required, logout_user, UserMixin
from datetime import datetime, time
import MySQLdb
import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)

import os

app.config["SECRET_KEY"] = os.urandom(24)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345"
app.config["MYSQL_DB"] = "red_social_2"
app.config["UPLOAD_POSTS_FOLDER"] = "uploads/posts"  # Carpeta para fotos de publicaciones
UPLOAD_FOLDER = 'uploads'
app.config["ALLOWED_EXTENSIONS"] = {"jpeg", "png", "jpg", "gif", "jfif"}
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirigir usuarios no autenticados al login



class User(UserMixin):
    def __init__(self, id, nombre="", apellidos="", fecha_nacimiento=None, Genero="", email="", passwordd="", foto_perfil=None, foto_portada=None):
        self.id = id  # Flask-Login requiere este atributo
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.Genero = Genero
        self.email = email
        self.passwordd = passwordd
        self.foto_perfil = foto_perfil
        self.foto_portada = foto_portada

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT 
            id_usuario, nombre, apellidos, fecha_nacimiento, Genero, email, passwordd, 
            COALESCE(foto_perfil, 'https://via.placeholder.com/100') AS foto_perfil, 
            COALESCE(foto_portada, 'https://via.placeholder.com/100') AS foto_portada 
        FROM Usuario 
        WHERE id_usuario = %s
        """,
        (user_id,),
    )
    user_data = cursor.fetchone()
    cursor.close()
    
    print(user_data)


    if user_data:
        
        # Asegúrate de mapear correctamente los datos del diccionario al constructor de la clase User
        return User(
            id=user_data['id_usuario'],
            nombre=user_data['nombre'],
            apellidos=user_data['apellidos'],
            fecha_nacimiento=user_data['fecha_nacimiento'],
            Genero=user_data['Genero'],
            email=user_data['email'],
            passwordd=user_data['passwordd'],
            foto_perfil=user_data['foto_perfil'],
            foto_portada=user_data['foto_portada']
        )
    return None



def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )

@app.route('/uploads/posts/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_POSTS_FOLDER'], filename)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def handle_image_upload(imagen):
    # Asegúrate de que el archivo sea válido
    if imagen and allowed_file(imagen.filename):
        try:
            # Crea un nombre único para la imagen
            filename = secure_filename(imagen.filename)
            image_name = f"{int(datetime.now().timestamp())}_{filename}"
            
            # Ruta donde se guardará la imagen
            image_path = os.path.join(app.config['UPLOAD_POSTS_FOLDER'], image_name)
            imagen.save(image_path)
            
            return image_name  # Devuelve el nombre de la imagen para guardarlo en la base de datos
        except Exception as e:
            flash(f"Error al subir la imagen: {str(e)}", "error")
            return None
        


# Ruta de inicio (pantalla de login)
@app.route("/")
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email y contraseña son obligatorios.", "error")
        return redirect(url_for("login"))

    
    cursor = mysql.connection.cursor()
    cursor.callproc("Usuarios_Logeo", (email,))
    result = cursor.fetchall()
    cursor.close()

    if len(result) > 0:
            user_data = result[0]
            stored_password = user_data[6]

            # Comparar contraseñas directamente
            if stored_password.strip() == password.strip():
                user = User(id=user_data[0], email=user_data[5])
                login_user(user)
                session["id_usuario"] = user_data[0]  
                session["email_usuario"] = user_data[5]  # Ejemplo de cómo guardar el email.

                # Redirige al feed o a otra página después del login exitoso
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for("feed"))  # Redirige al feed
            else:
                flash("Credenciales incorrectas.", "error")
    else:
        flash("Usuario no encontrado.", "error")
    

    return render_template("login.html")
    


@app.route("/nuevo_feed", methods=["POST"])
@login_required
def nuevo_feed():
    if not current_user.is_authenticated:
        flash("Debes iniciar sesión para publicar.", "error")
        return redirect(url_for("login"))  

    # Validar los datos del formulario
    content = request.form.get("content")
    if not content or len(content) > 500:
        flash(
            "El contenido es obligatorio y no debe exceder los 500 caracteres.", "error"
        )
        return redirect(url_for("feed"))  # O redirige a la página del feed

    # Procesar la imagen si existe
    image_name = None
    if "imagen" in request.files:
        imagen = request.files["imagen"]
        image_name = handle_image_upload(imagen)  
    
        # Insertar la publicación en la base de datos
        cur = mysql.connection.cursor()
        cur.callproc(
            "Crear_Publicacion",
            (current_user.id, content, image_name, datetime.utcnow()),
        )
        mysql.connection.commit()
        cur.close()

        flash("Publicación creada exitosamente.", "success")
        return redirect(url_for("feed"))



# Ruta protegida (feed)
@app.route("/feed")
@login_required
def feed():
    # Obtener al usuario autenticado
    usuario = current_user
    id_usuario = current_user.id

    if not usuario.is_authenticated:
        flash("Usuario no autenticado.", "error")
        return redirect(url_for("login"))

    
        # Obtener las publicaciones llamando al procedimiento almacenado
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc("obtener_publicaciones")
    publicaciones = cursor.fetchall()
    cursor.close()

        # Procesar cada publicación para incluir la reacción del usuario
    for publicacion in publicaciones:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
                """
                SELECT reaccion 
                FROM likes 
                WHERE id_usuario = %s AND id_publicacion = %s
            """,
                (usuario.id, publicacion["id_publicacion"]),
            )
        reaccion = cursor.fetchone()
        cursor.close()

        publicacion["reaccion_usuario"] = reaccion["reaccion"] if reaccion else None

        # Inicializar estructuras para comentarios y reacciones
        comentarios = {}
        reacciones = {}

        for publicacion in publicaciones:
            id_publicacion = publicacion["id_publicacion"]

            # Obtener los comentarios de cada publicación
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.callproc("obtener_comentarios", (id_publicacion,))
            comentarios[id_publicacion] = cursor.fetchall()
            cursor.close()

            # Obtener las reacciones de cada publicación
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.callproc("ObtenerReacciones", (id_publicacion,))
            reacciones[id_publicacion] = cursor.fetchall()
            cursor.close()
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.callproc("ObtenerAmigosPorID", (id_usuario,))
            amigos = cursor.fetchall()
            cursor.close()  # Esto debería devolver una lista de amigos
        

        # Renderizar la plantilla con las publicaciones, comentarios y reacciones
        return render_template(
            "feed.html",
            publicaciones=publicaciones,
            comentarios=comentarios,
            reacciones=reacciones,
            amigos=amigos
        )

    


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validaciones del formulario
        nombres = request.form.get("Nombres")
        apellidos = request.form.get("Apellidos")
        birthday_day = request.form.get("birthday_day")
        birthday_month = request.form.get("birthday_month")
        birthday_year = request.form.get("birthday_year")
        sex = request.form.get("sex")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirmation")

        # Validación básica
        if (
            not nombres
            or not apellidos
            or not birthday_day
            or not birthday_month
            or not birthday_year
            or not sex
            or not email
            or not password
        ):
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("register"))

        if password != password_confirm:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("register"))

        # Formato de fecha
        try:
            birthday = datetime(
                year=int(birthday_year),
                month=int(birthday_month),
                day=int(birthday_day),
            ).strftime("%Y-%m-%d")
        except ValueError:
            flash("Fecha de nacimiento no válida.", "error")
            return redirect(url_for("register"))
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.callproc(
                "Crear_Nuevo_usuario",
                [nombres, apellidos, birthday, sex, email, password],
            )
            mysql.connection.commit()  # Confirmar la transacción
            cursor.close()

            flash("Registro exitoso", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash(f"Error al registrar el usuario: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/reaccionar/<int:id_publicacion>", methods=["POST"])
@login_required
def reaccionar(id_publicacion):
    id_usuario = current_user.id
    tipo_reaccion = request.form.get("tipo")

    try:
        cursor = mysql.connection.cursor()

        # Ejecutamos el procedimiento almacenado para agregar la reacción
        cursor.callproc(
            "agregar_reacciones", (tipo_reaccion, id_usuario, id_publicacion)
        )
        mysql.connection.commit()

        # Contamos las reacciones
        cursor.execute(
            "SELECT COUNT(*) FROM likes WHERE id_publicacion = %s AND reaccion = %s",
            (id_publicacion, "me gusta"),
        )
        me_gusta = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM likes WHERE id_publicacion = %s AND reaccion = %s",
            (id_publicacion, "me encanta"),
        )
        me_encanta = cursor.fetchone()[0]

        cursor.close()

        flash("Reacción agregada correctamente.", "success")

        return redirect(url_for("feed"))
    
    except Exception as e:
        flash(f"Hubo un problema al agregar la reacción: {str(e)}", "error")
        return redirect(url_for("feed"))


@app.route("/comentar/<int:id_publicacion>", methods=["POST"])
@login_required
def comentar(id_publicacion):
    contenido = request.form.get("contenido")
    id_usuario = current_user.id  # Obtener el id del usuario autenticado

    # Verificar que el contenido no esté vacío
    if not contenido:
        flash("El contenido del comentario es obligatorio.", "error")
        return redirect(
            url_for("feed")
        )  # O la página donde se está mostrando la publicación

    try:
        # Establecer conexión con la base de datos
        cursor = mysql.connection.cursor()

        # Llamar al procedimiento almacenado para agregar el comentario
        cursor.callproc(
            "Agregar_Comentario",
            (
                id_publicacion,
                id_usuario,
                contenido,
                datetime.now().strftime("%Y-%m-%d"),
            ),
        )

        # Confirmar la transacción
        mysql.connection.commit()

        # Cerrar el cursor
        cursor.close()

        # Mensaje de éxito
        flash("Comentario agregado correctamente.", "success")
        return redirect(
            url_for("feed")
        )  # O redirige a la página de la publicación donde se hizo el comentario

    except Exception as e:
        flash(f"Hubo un problema al agregar el comentario: {str(e)}", "error")
        return redirect(url_for("feed"))
@app.route("/amigos")
@login_required
def amigos():
    
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return "Usuario no autenticado", 401
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Obtener amigos del usuario actual
    query = """
        SELECT usuario.*
        FROM amigos
        JOIN usuario
        ON (amigos.id_usuario1 = usuario.id_usuario AND amigos.id_usuario2 = %s)
        OR (amigos.id_usuario2 = usuario.id_usuario AND amigos.id_usuario1 = %s)
        WHERE amigos.estado = 'aceptado'; 
        """
    cursor.execute(query, (id_usuario, id_usuario))
        
    friends = cursor.fetchall()

        # Cerrar el cursor
    cursor.close()

    return render_template("Amigos.html", friends=friends)

    


# Ruta para ver los detalles de un perfil
@app.route("/perfil/<int:id_usuario>")
@login_required
def perfil(id_usuario):
    try:
        # Obtener datos del usuario llamando al procedimiento almacenado
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("ObtenerPerfilUsuario", [id_usuario])
        usuario_result = cursor.fetchall()
        cursor.close()
        
        if not usuario_result:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for("feed"))
        
        usuario = usuario_result[0] 
        
        tab = request.args.get('tab', 'publicaciones')

        # Obtener publicaciones del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("Listar_Publicaciones", [id_usuario])
        publicaciones = cursor.fetchall()
        cursor.close()

        # Obtener amigos del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("ObtenerAmigosporID", [id_usuario])
        amigos = cursor.fetchall()
        cursor.close()

        # Obtener fotos del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("ObtenerFotosporID", [id_usuario])
        fotos = cursor.fetchall()
        cursor.close()

        # Renderizar la plantilla con los datos obtenidos
        return render_template(
            "perfil_usuario.html",
            usuario=usuario, tab=tab,
            publicaciones=publicaciones,
            amigos=amigos,
            fotos=fotos
        )
    except Exception as e:
        flash(f"Error al cargar el perfil: {str(e)}", "error")
        return redirect(url_for("feed"))

@app.route('/enviar_solicitudes')
def enviar_solicitudes():
    try:
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return "Usuario no autenticado", 401

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc('ListarUsuariosDisponibles', [id_usuario])
        users = cursor.fetchall()
        cursor.close()
        
        return render_template('EnviarSolicitudes.html', users=users)
    except Exception as e:
        app.logger.error(f"Error en /enviar_solicitudes: {str(e)}")
        return "Error interno del servidor", 500
    
@app.route('/enviar_solicitud/<int:receiver_id>', methods=['POST'])
def enviar_solicitud(receiver_id):
    
        sender_id = session.get('id_usuario')
        if not sender_id:
            return jsonify({"message": "Usuario no autenticado"}), 401

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Verificar si ya existe una solicitud pendiente
        query = """
        SELECT 1
        FROM solicitudes
        WHERE enviado_id = %s AND recivido_id = %s AND status = 'pendiente';
        """
        cursor.execute(query, (sender_id, receiver_id))
        existing_solicitud = cursor.fetchone()

        if existing_solicitud:
            return jsonify({"message": "Ya existe una solicitud pendiente"}), 400

        # Llamar al procedimiento almacenado
        try:
            cursor.callproc('EnviarSolicitud', [sender_id, receiver_id])
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"message": f"Error al enviar solicitud: {str(e)}"}), 500

        cursor.close()
        return jsonify({"message": "Solicitud enviada exitosamente"}), 200
    
@app.route('/solicitudes_recibidas')
def received_requests():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return "Usuario no autenticado", 401

    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Consulta para obtener solicitudes recibidas pendientes
    query = """
        SELECT usuario.*
        FROM solicitudes
        JOIN usuario ON solicitudes.enviado_id = usuario.id_usuario
        WHERE solicitudes.recivido_id = %s AND solicitudes.status = 'pendiente';
        """
    cursor.execute(query, (id_usuario,))
    requests = cursor.fetchall()

    cursor.close()
    return render_template('Solicitudes.html', requests=requests)

@app.route('/aceptar_solicitud/<int:sender_id>', methods=['POST'])
def accept_request(sender_id):
    
        receiver_id = session.get('id_usuario')
        if not receiver_id:
            return jsonify({"message": "Usuario no autenticado"}), 401

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("SET @message = '';")

        # Llamar al procedimiento almacenado para aceptar la solicitud
        cursor.callproc('AceptarSolicitud', [sender_id, receiver_id, '@message'])
        mysql.connection.commit()

        # Ejecutar una consulta para obtener el valor del parámetro de salida
        cursor.execute("SELECT @message AS message;")
        result = cursor.fetchone()
        message = result['message'] if result and result['message'] else 'Solicitud procesada'
        

        cursor.close()
        return jsonify({"message": message}), 200
    
@app.route("/actualizar_foto_perfil", methods=["POST"])
def actualizar_foto_perfil():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        flash("Por favor, inicia sesión primero.", "error")
        return redirect(url_for('login'))
    if "foto_perfil" not in request.files:
        flash("No se ha seleccionado archivo", "error")
        return redirect(request.url)

    file = request.files['foto_perfil']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        foto_nombre = f"{int(time.time())}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile', foto_nombre))

        cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado en la base de datos
        cursor.callproc('actualizarFotoPerfil', (id_usuario, foto_nombre))
        mysql.connection.commit()
        cursor.close()

        flash("Foto de perfil actualizada exitosamente", "success")
        return redirect(url_for("Usuario"))

    else:
        flash("Formato de archivo no permitido. Solo se permiten archivos PNG, JPG y JPEG.", "error")
        return redirect(request.url)

@app.route("/actualizar_foto_portada", methods=["POST"])
def actualizar_foto_portada():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        flash("Por favor, inicia sesión primero.", "error")
        return redirect(url_for('login'))
    
    if "foto_portada" not in request.files:
        flash("No se ha seleccionado archivo", "error")
        return redirect(request.url)

    file = request.files['foto_portada']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        foto_nombre = f"{int(time.time())}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'covers', foto_nombre))
        
        cursor = mysql.connection.cursor()
        cursor.callproc('actualizarFotoPortada', (id_usuario, foto_nombre))
        mysql.connection.commit()
        cursor.close()

        flash("Foto de portada actualizada exitosamente", "success")
        return redirect(url_for("Usuario"))

    
    else:
        flash("Formato de archivo no permitido. Solo se permiten archivos PNG, JPG y JPEG.", "error")
        return redirect(request.url)


@app.route("/editar_perfil", methods=["POST"])
def editar_perfil():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]

    try:
        
        # Llamar al procedimiento almacenado para actualizar el perfil
        cursor = mysql.connection.cursor()

        cursor.callproc(
            "ActualizarPerfilUsuario", (current_user.id, nombre, apellidos,fecha_nacimiento, genero)
        )
        
        current_user.nombre = nombre
        current_user.apellidos = apellidos
        current_user.fecha_nacimiento = fecha_nacimiento
        current_user.genero = genero
        
        mysql.connection.commit()  # Confirmar los cambios en la base de datos

        flash("Perfil actualizado exitosamente", "success")
        
        # Redirigir al perfil del usuario para mostrar los cambios
        return redirect(url_for('Usuario'))

    except Exception as e:
        mysql.connection.rollback()  # Revertir en caso de error
        flash(f"Error al actualizar el perfil: {str(e)}", "error")
        
        # Redirigir de nuevo al perfil del usuario en caso de error
        return redirect(url_for('Usuario'))

    

@app.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    query = request.args.get('query')
    if not query or len(query) < 3:
        return jsonify({'error': 'El término de búsqueda debe tener al menos 3 caracteres'}), 400

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("BuscarClientes", [query])
        usuarios = cursor.fetchall()
        cursor.close()

        if not usuarios:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify(usuarios) 

    except Exception as e:
        return jsonify({'error': 'Error al realizar la búsqueda', 'message': str(e)}), 500

@app.route("/reacciones/<int:id_publicacion>", methods=["GET"])
@login_required
def obtenerReacciones(id_publicacion):
    try:
        cursor = mysql.connection.cursor()

        # Consulta para obtener los usuarios y sus reacciones
        cursor.execute("""
            SELECT u.nombre AS usuario_nombre, u.foto_perfil, r.reaccion
            FROM usuario u
            JOIN likes r ON u.id_usuario = r.id_usuario
            WHERE r.id_publicacion = %s
        """, (id_publicacion,))
        usuarios_reacciones = cursor.fetchall()

        # Convertir los resultados a una lista de diccionarios
        reacciones = [
            {"usuario_nombre": usuario[0], "foto_perfil": usuario[1], "reaccion": usuario[2]}
            for usuario in usuarios_reacciones
        ]

        cursor.close()

        # Respuesta JSON con los datos de las reacciones
        return jsonify({"reacciones": reacciones}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/eliminar_amigo/<int:amigo_id>", methods=["GET"])
def eliminar_amigo(amigo_id):
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        flash("Por favor, inicia sesión primero.", "error")
        return redirect(url_for('login'))
    
    # Llamar al procedimiento almacenado para eliminar el amigo
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc("EliminarAmigo", (id_usuario, amigo_id))
    mysql.connection.commit()
    cursor.close()

    flash("Amigo eliminado con éxito.", "success")
    return redirect(url_for('amigos'))

@app.route("/Usuario", methods=["GET"])
def Usuario():
    
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            flash("Por favor, inicia sesión primero.", "error")
            return redirect(url_for('login'))
        
        tab = request.args.get('tab', 'publicaciones')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.callproc("ObtenerPerfilUsuario", (id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()

        if not usuario:
            flash("El perfil del usuario no se pudo cargar.", "error")
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("Listar_Publicaciones", (id_usuario,))
        publicaciones = cursor.fetchall()
        cursor.close()


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("ObtenerAmigosPorID", (id_usuario,))
        amigos = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc("ObtenerFotosPorID", (id_usuario,))
        fotos = cursor.fetchall()
        cursor.close()
        
        # Renderizar la plantilla con los datos obtenidos
        return render_template('Usuario.html', tab=tab, usuario=usuario, publicaciones=publicaciones, amigos=amigos, fotos=fotos, foto_perfil=usuario['foto_perfil'], foto_portada=usuario['foto_portada'])

@app.route("/amistades", methods=["GET"])
@login_required
def obtener_amigos():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT nombre, foto_perfil 
            FROM usuario 
            WHERE id_usuario IN (SELECT amigo_id FROM amistades WHERE usuario_id = %s)
        """, (current_user.id,))
        amigos = cursor.fetchall()

        amigos_data = [{"nombre": amigo[0], "foto_perfil": amigo[1]} for amigo in amigos]

        cursor.close()

        return jsonify(amigos_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat/<int:user_id>")
@login_required
def chat(user_id):
    try:
        # Primera conexión para información del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Usuario WHERE id_usuario = %s', [user_id])
        chat_user = cursor.fetchone()
        cursor.close()

        # Segunda conexión para mensajes
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc('sp_Mensaje_VerConversacion', [current_user.id, user_id])
        mensajes = cursor.fetchall()
        cursor.close()

        # Tercera conexión para lista de amigos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc('sp_Amigos_ConMensajes', [current_user.id])
        amigos = cursor.fetchall()
        cursor.close()

        if chat_user:
            return render_template("chat.html", 
                                chat_user=chat_user,
                                mensajes=mensajes,
                                amigos=amigos)
        return redirect(url_for('feed'))
        
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('feed'))

@app.route("/chat/<int:user_id>/enviar", methods=['POST'])
@login_required
def enviar_mensaje(user_id):
    data = request.get_json()
    mensaje = data.get('mensaje')
    
    if mensaje:
        cursor = mysql.connection.cursor()
        cursor.callproc('sp_Mensaje_Enviar', [current_user.id, user_id, mensaje])
        mysql.connection.commit()
        cursor.close()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route("/chat/<int:user_id>/actualizar", methods=['GET'])
@login_required
def actualizar_mensajes(user_id):
    ultimo_id = request.args.get('ultimo_id', 0, type=int)
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('sp_Mensaje_MarcarComoLeidos', [current_user.id, user_id, ultimo_id])
    mensajes_nuevos = cursor.fetchall()
    cursor.close()
    
    return jsonify({'mensajes': mensajes_nuevos})

# Ruta de cierre de sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
