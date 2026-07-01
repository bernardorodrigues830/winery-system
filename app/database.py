from sqlmodel import SQLModel, Session, create_engine, event
from sqlalchemy import event as sa_event

DATABASE_URL = "sqlite:///./winery.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

# Ativa checagem de FK no SQLite (desligada por padrão)
@sa_event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session