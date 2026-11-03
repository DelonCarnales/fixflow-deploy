from database import normalize_database_url


def test_postgres_scheme_is_rewritten_for_sqlalchemy():
    assert normalize_database_url("postgres://user:pw@host:5432/db") == "postgresql://user:pw@host:5432/db"


def test_other_urls_are_left_unchanged():
    assert normalize_database_url("postgresql://user:pw@host/db") == "postgresql://user:pw@host/db"
    assert normalize_database_url("postgresql+psycopg2://user:pw@host/db") == "postgresql+psycopg2://user:pw@host/db"
    assert normalize_database_url("sqlite:///./fixflow.db") == "sqlite:///./fixflow.db"
