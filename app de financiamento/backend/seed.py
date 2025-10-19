from .database import SessionLocal, engine
from . import models, crud, auth
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
if not crud.get_user_by_email(db, 'admin@financontrol.local'):
    admin = crud.create_user(db, email='admin@financontrol.local', hashed_password=auth.get_password_hash('admin123'), full_name='Admin', is_admin=True)
    print('Admin criado:', admin.email)
else:
    print('Admin já existe')
c1 = crud.create_client(db, 'João Silva', 'joao@example.com', '1199999')
c2 = crud.create_client(db, 'Maria Santos', 'maria@example.com', '1198888')
crud.create_loan(db, client_id=c1.id, amount=1200, term_months=12)
crud.create_loan(db, client_id=c2.id, amount=2400, term_months=6)
print('Seed concluído')
