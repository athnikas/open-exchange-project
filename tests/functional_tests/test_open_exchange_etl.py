import os
from dotenv import load_dotenv
from src.readers.api.open_exchange import OpenExchangeConnector
from src.pipelines.openexchange_pipeline import run_etl, _transform
import pandas as pd
from src.models import CurrencyExchangeRate
from sqlalchemy import create_engine, select

# Load environment variables from .env file
load_dotenv()

# Get environment variables
APP_ID = os.getenv('APP_ID')
TEST_DATABASE_URL = os.getenv('DATABASE_URL')

def test_run_etl_for_multiple_dates():
    # Define the dates for ETL process
    dates = ['2024-05-12', '2024-05-13', '2024-05-14']

    # Connect to the test database
    engine = create_engine(TEST_DATABASE_URL)
    api_conn = OpenExchangeConnector(app_id=APP_ID, base="USD")

    for date in dates:
        # Run the ETL process for each date
        run_etl(date)

        # Fetch data from the API

        api_data = api_conn.extract_data(date=date)

        # Transform API data
        transformed_api_data = _transform(api_data, date)

        # Verify that data is successfully loaded into the test database
        with engine.connect() as conn:
            stmt = select(CurrencyExchangeRate).where(CurrencyExchangeRate.currency_date == date)
            result = conn.execute(stmt)
            db_rows = result.fetchall()

        # Compare the count of loaded data and API transformed data
        assert len(db_rows) == len(transformed_api_data)

        # # Check if all data is loaded by checking if any rows have different values
        db_df = pd.DataFrame(db_rows).set_index('currency_symbol')[['currency_date', 'currency_rate']].sort_index()
        api_df = pd.DataFrame(transformed_api_data).set_index('currency_symbol')[['currency_date', 'currency_rate']].sort_index()

        pd.testing.assert_frame_equal(db_df, api_df)   