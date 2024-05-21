
CREATE OR REPLACE VIEW public.v_currency_exchange_rate_current
 AS
 SELECT currency_symbol,
    currency_date,
    currency_rate,
    load_timestamp
   FROM currency_exchange_rate
  WHERE currency_date = CURRENT_DATE;