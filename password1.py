from flask import Flask
from flask_bcrypt import Bcrypt

# Inicializar la aplicación Flask
app = Flask(__name__)

# Crear instancia de Bcrypt para encriptar contraseñas
seguridad = Bcrypt(app)

# Contraseña en texto plano
clave_original = "mi_contraseña_ super secreta es "

# Generar hash seguro de la contraseña
clave_hash = seguridad.generate_password_hash(clave_original).decode('utf-8')

# Mostrar el resultado
print("Contraseña convertida a hash:", clave_hash)
