from sqlalchemy import Column, Double, String, Date, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime as dt


Base = declarative_base()


class CurrencyExchangeRate(Base):
    __tablename__ = 'currency_exchange_rate'
    currency_symbol = Column(String, primary_key=True)
    currency_date = Column(Date, primary_key=True)
    currency_rate = Column(Double, nullable=False)
    load_timestamp = Column(DateTime, nullable=False, default=dt.now())
