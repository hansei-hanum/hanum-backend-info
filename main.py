from fastapi import FastAPI
from routes import include_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from neis import Meal
import time

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        {"message": exc.detail, "data": None}, status_code=exc.status_code
    )


@app.on_event("startup")
async def startup_event():
    pass


include_router(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
