import json
import os
import pandas as pd
from src.readers.api.open_exchange import OpenExchangeConnector
from src.writers.postgres_writer import PostgresWriter
from src.models import CurrencyExchangeRate
from src.validators.validators import validate_schema
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')
DATABASE_URL = os.getenv('DATABASE_URL')


def _convert_exchange_basis(df, basis="EUR"):
    basis_rate = df.loc[df['currency_symbol']
                        == basis, 'currency_rate'].values[0]
    df["currency_rate"] = df["currency_rate"] / basis_rate

    return df


def _extract(api_conn, date):
    return api_conn.extract_data(date=date)


def _transform(data, date):
    df = pd.DataFrame.from_dict(data).reset_index(
            names='currency')[["currency", "rates"]].copy()
    
    df.rename(columns={
        "currency": "currency_symbol",
        "rates": "currency_rate"
    },
        inplace=True)
    
    df["currency_date"] = date

    df = _convert_exchange_basis(df, basis="EUR")

    return json.loads(df.to_json(orient='records'))


def _load(data):
    engine = create_engine(DATABASE_URL)
    db_conn = PostgresWriter(engine=engine)
    db_conn.upsert(CurrencyExchangeRate, data,
    index_elements=["currency_symbol", "currency_date"])

def run_etl(date):

    api_conn = OpenExchangeConnector(
            app_id=APP_ID, 
            base="USD"
            )

    data = _extract(api_conn, date)

    validate_schema(data)

    data = _transform(data, date)

    _load(data)
 
        