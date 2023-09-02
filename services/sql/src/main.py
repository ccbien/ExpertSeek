import os
import traceback

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from core import Database
from config import settings

db = None
app = FastAPI(title="SQL Database service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.on_event("startup")
def startup_event():
    global db
    db = Database(settings.DB_PATH)


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


@app.get("/get/paper")
def get_paper(paper_id: str):
    try:
        paper = db.get_paper(paper_id)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "paper": paper})


@app.get("/get/author")
def get_author(author_id: str):
    try:
        author = db.get_author(author_id)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "author": author})


@app.get("/get/top-coauthor")
def get_top_coauthors(author_id: str, limit: int):
    try:
        authors = db.get_top_coauthors(author_id, limit)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "authors": authors})


@app.get("/get/num-citations")
def get_num_citations(author_id: str):
    try:
        n_citation = db.get_num_citations(author_id)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "n_citation": n_citation})


@app.get("/get/all-papers")
def get_all_papers(author_id: str):
    try:
        papers = db.get_all_papers(author_id)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "papers": papers})


@app.get("/search/authors")
def search_authors(name: str, org: str, limit: int):
    try:
        authors = db.search_authors(name, org, limit)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "authors": authors})


@app.get("/get/first-author")
def get_first_author(paper_id: str):
    try:
        author_id = db.get_first_author(paper_id)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content={"message": "SQL Database error"})

    return JSONResponse(content={"message": "success", "author_id": author_id})


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT)
