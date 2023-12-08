from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from . import models
from .database import check_database_connection, engine
from .routers import  user, auth, federated, fedavg


models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(federated.router)
app.include_router(fedavg.router)


@app.get("/")
def root() -> dict:
    try:
        health_check_passed = check_database_connection()

        if not health_check_passed:
            raise Exception("Database health check failed")

        message = "Server is Running and Good"
        return {"status": "success", "message": message}

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
