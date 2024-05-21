import argparse
from datetime import datetime as dt, timedelta
from src.validators.validators import validate_arguments
from src.pipelines.openexchange_pipeline import run_etl


if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description='Simple ETL app')

    parser.add_argument('--start_date', default=dt.now().strftime("%Y-%m-%d"))
    parser.add_argument('--end_date', default=dt.now().strftime("%Y-%m-%d"))

    # # Now, parse the command line arguments and store the
    # # values in the `args` variable
    args = parser.parse_args()
    validate_arguments(args.start_date, args.end_date)

    date = args.start_date
    while date <= args.end_date:

        run_etl(date)

        date = dt.strptime(date, "%Y-%m-%d")
        date += timedelta(days=1)
        date = dt.strftime(date, "%Y-%m-%d")
