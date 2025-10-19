import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, crud, database, auth, config
from .database import engine
from pathlib import Path
import shutil
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="FinanControl API", version="2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_FOLDER = Path(config.UPLOAD_FOLDER)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
static_dir = Path(__file__).resolve().parent.parent / 'frontend' / 'static'
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_FOLDER)), name="uploads")
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post('/register')
def register(email: str, password: str, full_name: str = '', db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail='Email já registrado')
    hashed = auth.get_password_hash(password)
    user = crud.create_user(db, email=email, hashed_password=hashed, full_name=full_name, is_admin=False)
    return {'id': user.id, 'email': user.email, 'full_name': user.full_name}
@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Usuário ou senha incorretos')
    access_token = auth.create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
@app.get('/me')
def me(current_user: models.User = Depends(auth.get_current_user)):
    return {'id': current_user.id, 'email': current_user.email, 'full_name': current_user.full_name}
@app.post('/clients')
def create_client(name: str, email: str = '', phone: str = '', db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_client(db, name=name, email=email or None, phone=phone or None)
@app.get('/clients')
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_clients(db, skip, limit)
@app.post('/loans')
def create_loan(client_id: int, amount: float, term_months: int = 1, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    return crud.create_loan(db, client_id=client_id, amount=amount, term_months=term_months)
@app.get('/loans')
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_loans(db, skip, limit)
@app.post('/upload-thumbnail')
def upload_thumbnail(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    filename = file.filename
    dest = UPLOAD_FOLDER / filename
    with dest.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'url': f'/uploads/{filename}'}
@app.get('/static-app.zip')
def get_static_zip():
    static_zip = Path(__file__).resolve().parent.parent / 'frontend' / 'FinanControl_v2.zip'
    if static_zip.exists():
        return FileResponse(static_zip, media_type='application/zip', filename='FinanControl_v2.zip')
    raise HTTPException(status_code=404, detail='ZIP não encontrado')
