from app.clients.database import PostgresClient


def test_pytest_is_working():
    assert True


def test_app_is_importable():
    from app.app import app

    assert app is not None


def test_postgres_client_db_generator():
    db_gen = PostgresClient.db()
    db = next(db_gen)

    assert db is not None

    try:
        next(db_gen)
    except StopIteration:
        pass
