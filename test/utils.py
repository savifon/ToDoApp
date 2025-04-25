import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from models import ToDos


# Banco de teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test/testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação do banco ANTES de rodar app
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Agora sim importa o app (que monta os routers)
from main import app

# Override das dependências
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'saviotest', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    todo = ToDos(
        title="Learn to code!",
        description="Need to learn every day!",
        priority=5,
        complete=True,
        owner_id=1
    )
    db.add(todo)
    db.commit()
    db.close()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()