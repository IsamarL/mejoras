from cryptography.fernet import Fernet

# Texto que se desea proteger
mensaje = "x?1_p-M.4!eM"

# Generar una nueva clave y crear un objeto Fernet
clave_segura = Fernet.generate_key()
fernet_instancia = Fernet(clave_segura)

# Encriptar el mensaje
mensaje_cifrado = fernet_instancia.encrypt(mensaje.encode())
print(f"Mensaje cifrado: {mensaje_cifrado}")

# Desencriptar para recuperar el mensaje original
mensaje_descifrado = fernet_instancia.decrypt(mensaje_cifrado).decode()
print(f"Mensaje descifrado correctamente: {mensaje_descifrado}")
