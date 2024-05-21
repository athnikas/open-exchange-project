import pytest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from src.writers.postgres_writer import PostgresWriter
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Define a simple test table schema
metadata = MetaData()
test_table = Table('test_table', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('value', Integer))

# Define the test data
test_data = [
    {'id': 1, 'name': 'A', 'value': 10},
    {'id': 2, 'name': 'B', 'value': 20},
    {'id': 3, 'name': 'C', 'value': 30}
]

duplicate_data = [
    {'id': 1, 'name': 'A', 'value': 10},
    {'id': 1, 'name': 'A', 'value': 10},
    {'id': 3, 'name': 'C', 'value': 30}
]

@pytest.fixture(scope="module")
def engine():
    # Create a PostgreSQL database for testing
    engine = create_engine('postgresql+psycopg2://thanos:1312@localhost/postgres')
    metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def session(engine):
    # Create a session for interacting with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_upsert(engine, session):
    writer = PostgresWriter(engine)
    writer.upsert(test_table, test_data, ['id'])

    # Verify that the data has been correctly upserted
    rows = session.query(test_table).all()
    assert len(rows) == len(test_data)
    for row in rows:
        assert {'id': row.id, 'name': row.name, 'value': row.value} in test_data

def test_upsert_with_rollback(engine, session):
    # Create a writer instance
    writer = PostgresWriter(engine)

    try:
        writer.upsert(test_table, duplicate_data, ['id'])
    except Exception as e:
        pass  # Handle the exception if needed

    # Verify that no rows were inserted into the session
    rows = session.query(test_table).all()
    assert len(rows) == 3  # Only the initial rows should remain



