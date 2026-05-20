from fastapi import FastAPI
from routers import auth, notas, ia
from config import PORT
from dependencies import get_current_user

app = FastAPI(title="API IA-ready de Notas")

app.include_router(auth.router)
app.include_router(notas.router)
app.include_router(ia.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)