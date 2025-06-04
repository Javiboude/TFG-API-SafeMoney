from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa los routers específicamente
from app.api.endpoints.usuarioRouter import router as usuario_router
from app.api.endpoints.contactoRouter import router as contacto_router
from app.api.endpoints.movimientoRouter import router as movimiento_router
from app.api.endpoints.tarjetaRouter import router as tarjeta_router
from app.api.endpoints.transaccionRouter import router as transaccion_router

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers con el prefijo /api
app.include_router(usuario_router, prefix="/api")
app.include_router(contacto_router, prefix="/api")
app.include_router(movimiento_router, prefix="/api")
app.include_router(tarjeta_router, prefix="/api")
app.include_router(transaccion_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)