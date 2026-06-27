from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./winery.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite
    echo=True,  # mostra o SQL gerado no terminal (útil para aprender)
)

def create_db_and_tables():
    """Cria todas as tabelas no banco. Chamada uma vez na inicialização."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependência do FastAPI: abre e fecha a sessão automaticamente."""
    with Session(engine) as session:
        yield session