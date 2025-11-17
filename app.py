from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL

# =========================
# Inicialización de la app
# =========================
app = Flask(__name__)
app.secret_key = '09f78ead-8a13-11f0-9f04-089798bc6dda'

# ----------------- CONEXIÓN A MYSQL -----------------
app.config['MYSQL_HOST'] = 'bkm28yhgx1tke8ml3dca-mysql.services.clever-cloud.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'uhjjt644tkntmre3'
app.config['MYSQL_PASSWORD'] = 'lzdqe0dTidT4475nNeez'
app.config['MYSQL_DB'] = 'bkm28yhgx1tke8ml3dca'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# =========================
# RUTAS PRINCIPALES
# =========================
@app.route('/', methods=['GET', 'POST'])
def inicio():

    # ----------- POST (lo que pediste) -----------
    if request.method == 'POST':
        # Si el usuario está logueado
        if 'usuario' in session:
            if session.get('rol') == 1:
                return redirect(url_for('admin'))
            return render_template("index.html", usuario=session['usuario'])
        
        # Si no está logueado igual renderiza el inicio
        return render_template("index.html")

    # ----------- GET (Render lo necesita) -----------
    if 'usuario' in session:
        if session.get('rol') == 1:
            return redirect(url_for('admin'))
        return render_template("index.html", usuario=session['usuario'])

    return render_template("index.html")


@app.route('/acercade')
def acercade():
    return render_template("acercade.html")


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    user = {'nombre': '', 'email': '', 'mensaje': ''}
    if request.method == 'GET':
        user['nombre'] = request.args.get('nombre', '')
        user['email'] = request.args.get('email', '')
        user['mensaje'] = request.args.get('mensaje', '')
    return render_template("contacto.html", usuario=user)


@app.route('/contactopost', methods=['GET', 'POST'])
def contactopost():
    user = {'nombre': '', 'email': '', 'mensaje': ''}
    if request.method == 'POST':
        user['nombre'] = request.form.get('nombre', '')
        user['email'] = request.form.get('email', '')
        user['mensaje'] = request.form.get('mensaje', '')
    return render_template("contactopost.html", usuario=user)


# =========================
# LOGIN / REGISTRO / LOGOUT
# =========================
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/accesologin', methods=['POST'])
def accesologin():
    email = request.form.get('email')
    password = request.form.get('password')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM usuario WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()

    if user:
        session['usuario'] = user['email']
        session['rol'] = user['id_rol']
        flash('Inicio de sesión correcto. ¡Bienvenido!', 'success')
        if user['id_rol'] == 1:
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("inicio"))
    else:
        flash('Usuario y Contraseña incorrecta', 'danger')
        return render_template("login.html")


@app.route('/Registro', methods=['GET', 'POST'])
def Registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        id_rol = 2

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO usuario (email, nombre, password, id_rol) VALUES (%s, %s, %s, %s)",
                        (email, nombre, password, id_rol))
            mysql.connection.commit()

        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template("Registro.html")


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada con éxito.', 'info')
    return redirect(url_for('inicio'))


# =========================
# PANEL ADMIN CON CONTADORES
# =========================
@app.route('/admin')
def admin():
    if 'usuario' in session and session.get('rol') == 1:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total_usuarios FROM usuario")
            total_usuarios = cur.fetchone()['total_usuarios']

            cur.execute("SELECT COUNT(*) AS total_productos FROM producto")
            total_productos = cur.fetchone()['total_productos']

        return render_template('admin.html',
                               total_usuarios=total_usuarios,
                               total_productos=total_productos)
    else:
        flash('Debes iniciar sesión como administrador para acceder al panel', 'warning')
        return redirect(url_for('login'))


# =========================
# LISTAR USUARIOS (CRUD)
# =========================
@app.route('/listar')
def listar():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()
    return render_template("listar.html", usuarios=usuarios)


@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    id_rol = 2
    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO usuario (nombre, email, password, id_rol) VALUES (%s, %s, %s, %s)",
                    (nombre, email, password, id_rol))
        mysql.connection.commit()
    flash('Usuario agregado correctamente', 'success')
    return redirect(url_for('listar'))


@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    id = request.form['id']
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE usuario SET nombre=%s, email=%s, password=%s WHERE id=%s",
                    (nombre, email, password, id))
        mysql.connection.commit()
    flash('Usuario actualizado correctamente', 'success')
    return redirect(url_for('listar'))


@app.route('/borrarUser/<int:id>')
def borrarUser(id):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
        mysql.connection.commit()
    flash('Usuario eliminado correctamente', 'question')
    return redirect(url_for('listar'))


# =========================
# LISTAR PRODUCTOS
# =========================
@app.route('/listar_productos')
def listar_productos():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM producto")
        productos = cur.fetchall()
    return render_template("listar_productos.html", productos=productos)


@app.route('/api/productos')
def api_productos():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM producto")
        data = cur.fetchall()
    return jsonify(data)


# =========================
# AGREGAR PRODUCTOS
# =========================
@app.route('/listar_productos_agregados', methods=['GET', 'POST'])
def listar_productos_agregados():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO producto (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
                        (nombre, descripcion, precio, stock))
            mysql.connection.commit()

        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('listar_productos'))

    return render_template("listar_productos_agregados.html")


# =========================
# PERFIL DE USUARIO
# =========================
@app.route('/usuario')
def usuario():
    if 'usuario' in session:
        return render_template("usuario.html", usuario=session['usuario'])
    else:
        flash('Debes iniciar sesión para acceder a tu perfil', 'warning')
        return redirect(url_for('login'))


# =========================
# CONTADOR DINÁMICO
# =========================
contador = 0

@app.route('/incrementar', methods=['POST'])
def incrementar():
    global contador
    contador += 1
    return jsonify({'contador': contador})


@app.route('/decrementar', methods=['POST'])
def decrementar():
    global contador
    contador -= 1
    return jsonify({'contador': contador})


# =========================
# MAIN
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=8000)
