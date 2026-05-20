import os 

SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-super-segura-cambiar-en-produccion")
PORT = int(os.getenv("PORT", 8000))