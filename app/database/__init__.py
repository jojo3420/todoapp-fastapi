from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {schema_name};")


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")


url = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_SCHEMA}"

# https://yujuwon.tistory.com/entry/SQLALCHEMY-session-%EA%B4%80%EB%A6%AC
# https://kjk3071.tistory.com/entry/DB-MySQL-timeout-%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0
engine = create_engine(url,
                       echo=settings.QUERY_DEBUG_MODE,
                       pool_recycle=settings.DB_POOL_RECYCLE,
                       pool_size=settings.DB_POOL_SIZE,
                       max_overflow=settings.DB_MAX_POOL_OVERFLOW,
                       pool_pre_ping=True
                       )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_conn():
    """create session and return db conn"""
    conn = SessionLocal()
    try:
        yield conn
    finally:
        conn.close()
