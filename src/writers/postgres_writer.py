from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class PostgresWriter:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        
    def upsert(self, table, rows, index_elements):
        stmt = insert(table).values(rows)
        update_dict = {col.name: col for col in stmt.excluded if col.name not in index_elements}
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_=update_dict
        )
        session = self.Session()
        try:
            session.execute(stmt)
            session.commit()
        except:
            session.rollback()

        finally:
            session.close()