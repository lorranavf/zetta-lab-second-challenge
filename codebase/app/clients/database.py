import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(encoding="utf-8")


class PostgresClient:
    _engine = None
    _session = None
    _base = None

    @classmethod
    def initialize(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                os.getenv("DATABASE_URL"), connect_args={"client_encoding": "utf8"}
            )
            cls._session = sessionmaker(
                autocommit=False, autoflush=False, bind=cls._engine
            )
            cls._base = declarative_base()

    @classmethod
    def base(cls):
        cls.initialize()
        return cls._base

    @classmethod
    def connect(cls):
        cls.initialize()
        return cls._base.metadata.create_all(bind=cls._engine)

    @classmethod
    def db(cls):
        cls.initialize()
        db = cls._session()
        try:
            yield db
        finally:
            db.close()
