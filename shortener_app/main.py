# shortener_app/main.py
import secrets
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code = 400, detail = message)


def raises_not_found(request):
    message = f"La URL '{request.url}' no existe"
    raise HTTPException(status_code=404, detail=message)


# definir la raiz
@app.get("/")
def read_root():
    return "Bienvenido a la API acortadora de URLs :)"


# definir entrada de datos
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):  # type: ignore
        raise_bad_request(message="La url indicada no es valida")
    
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


# definir la redirección
@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    db_url = (
        db.query(models.URL).filter(models.URL.key == url_key,
        models.URL.is_active).first()
        )
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raises_not_found(request)