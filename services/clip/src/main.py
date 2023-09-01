import os
import traceback

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from core import CLIPEncoder
from config import settings

clip_encoder = None
app = FastAPI(title="Jina CLIP service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.on_event("startup")
def startup_event():
    global clip_encoder
    clip_encoder = CLIPEncoder(
        settings.JINA_CLIP_ENDPOINT,
        settings.JINA_API_KEY
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    error_details = []
    for error in details:
        error_details.append({"error": error["msg"] + " " + str(error["loc"])})
    return JSONResponse(content={"message": error_details})


@app.get("/", include_in_schema=False)
def root() -> None:
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
def perform_healthcheck() -> None:
    return JSONResponse(content={"message": "success"})


@app.get("/encode")
def fetch(text: str):
    try:
        embedding = clip_encoder.encode(text)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "Jina CLIP error"})

    return JSONResponse(content={"message": "success", "embedding": embedding})


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT)
