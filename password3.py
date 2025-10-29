from passlib.context import CryptContext

# Configuración del cifrado
# Se utiliza pbkdf2_sha256 con 30,000 iteraciones
cifrado = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

# Contraseña a proteger
mi_clave = "x?1_p-M.4!eM"

# Generar el hash seguro
hash_clave = cifrado.hash(mi_clave)
print(f"Hash generado: {hash_clave}")

# Verificar si la contraseña coincide con el hash
coincidencia = cifrado.verify(mi_clave, hash_clave)
print(f"¿Contraseña correcta?: {coincidencia}")
