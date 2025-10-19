from sqlalchemy.orm import Session
from . import models
from typing import List, Optional
from sqlalchemy import func
def create_user(db: Session, email: str, hashed_password: str, full_name: Optional[str] = None, is_admin: bool = False):
    db_user = models.User(email=email, full_name=full_name, hashed_password=hashed_password, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
def create_client(db: Session, name: str, email: Optional[str] = None, phone: Optional[str] = None):
    db_client = models.Client(name=name, email=email, phone=phone)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()
def delete_client(db: Session, client_id: int):
    obj = db.query(models.Client).filter(models.Client.id == client_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
def create_loan(db: Session, client_id: int, amount: float, term_months: int = 1):
    db_loan = models.Loan(client_id=client_id, amount=amount, term_months=term_months)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
def get_loans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).offset(skip).limit(limit).all()
def get_loans_by_client(db: Session, client_id: int):
    return db.query(models.Loan).filter(models.Loan.client_id == client_id).all()
def update_loan_status(db: Session, loan_id: int, status: str):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if loan:
        loan.status = status
        db.commit()
        db.refresh(loan)
    return loan
def total_loan_value(db: Session):
    return db.query(func.sum(models.Loan.amount)).scalar() or 0
def loans_per_month(db: Session):
    q = db.query(func.strftime("%Y-%m", models.Loan.created_at).label("ym"), func.count(models.Loan.id), func.sum(models.Loan.amount)).group_by("ym").order_by("ym")
    return [{"month": r[0], "count": r[1], "total": r[2]} for r in q.all()]
