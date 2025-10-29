from werkzeug.security import generate_password_hash, check_password_hash

# Contraseña a proteger
clave = "x?1_p-M.4!eM"

# Generar el hash seguro de la contraseña
hash_clave = generate_password_hash(clave)
print(f"Hash generado: {hash_clave}")

# Verificar si la contraseña coincide con el hash
coincide = check_password_hash(hash_clave, clave)
print(f"¿La contraseña es correcta?: {coincide}")
