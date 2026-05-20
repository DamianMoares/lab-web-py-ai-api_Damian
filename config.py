import os 

SECRET_KEY= os.getenv("SECRET_KEY")
PORT= int (os.getenv("PORT",8000))