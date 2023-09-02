import os
import traceback
from typing import List

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from core import ZillizClient
from config import settings

class SearchRequest(BaseModel):
    vector: List[float]
    limit: int = 10
    

zilliz_client = None
app = FastAPI(title="Vector Database service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.on_event("startup")
def startup_event():
    global zilliz_client
    zilliz_client = ZillizClient(
        settings.ZILLIZ_ENDPOINT,
        settings.ZILLIZ_API_KEY
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


@app.post("/search/paper")
async def search_paper(search_request: SearchRequest):
    try:
        data = zilliz_client.search("papers", search_request.vector, search_request.limit)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "Vector Database error"})

    return JSONResponse(content={"message": "success", "data": data})


@app.post("/search/author")
async def search_author(search_request: SearchRequest):
    try:
        data = zilliz_client.search("authors", search_request.vector, search_request.limit)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "Vector Database error"})

    return JSONResponse(content={"message": "success", "data": data})


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT)
